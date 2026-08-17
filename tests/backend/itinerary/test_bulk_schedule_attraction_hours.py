from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import itinerary_animals_for_exhibits

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.data_access.attraction_record import AttractionRecord
from api.attractions.scheduling.attraction_operating_hours import attraction_has_configured_operating_hours
from api.attractions.scheduling.attraction_operating_hours import attraction_operating_hours_seconds
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.models.attraction import Attraction
from api.models.itinerary_transportation import ItineraryTransportation
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType
from conftest import DbControllers


KANGAROO = {
   'species': 'Western Grey Kangaroo',
   'exhibit': 'Australasia Outdoor',
}
WOMBAT = {
   'species': "Southern Hairy-Nosed Wombat",
   'exhibit': 'Australasia Pavilion',
   'enclosure_name': 'Outdoor',
}
AMUR_TIGER = {
   'species': 'Amur Tiger',
   'exhibit': 'Eurasia Wilds',
}
KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
SPLASH_ISLAND = 'Splash Island'


def _hours_payload(
      attraction: str,
      *,
      weekday_start: str,
      weekday_end: str,
      weekend_start: str,
      weekend_end: str ) -> dict:
   return {
      'attraction': attraction,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'weekday_start_time': weekday_start,
      'weekday_end_time': weekday_end,
      'weekend_holiday_start_time': weekend_start,
      'weekend_holiday_end_time': weekend_end,
   }


def test_attraction_operating_hours_falls_back_to_zoo_hours_when_unset() -> None:
   record = AttractionRecord(
      name='Splash Island',
      free_with_admission=True,
      description='',
      info_link='',
      hyperlink_text='',
      x_coord=0.0,
      y_coord=0.0,
      region='Discovery Zone',
      weekday_multiplier=1.0,
      weekend_holiday_multiplier=1.0 )

   assert not attraction_has_configured_operating_hours(
      record,
      visit_date=date( 2026, 6, 20 ) )
   assert attraction_operating_hours_seconds(
      record,
      visit_date=date( 2026, 6, 20 ),
      zoo_open_seconds=9 * 3600,
      zoo_close_seconds=18 * 3600 ) == ( 9 * 3600, 18 * 3600 )


def test_attraction_operating_hours_uses_weekend_pair() -> None:
   record = AttractionRecord(
      name='Splash Island',
      free_with_admission=True,
      description='',
      info_link='',
      hyperlink_text='',
      x_coord=0.0,
      y_coord=0.0,
      region='Discovery Zone',
      weekday_multiplier=1.0,
      weekend_holiday_multiplier=1.0,
      weekday_start_time='10:00 AM',
      weekday_end_time='4:00 PM',
      weekend_holiday_start_time='11:00 AM',
      weekend_holiday_end_time='5:00 PM' )

   assert attraction_has_configured_operating_hours(
      record,
      visit_date=date( 2026, 6, 20 ) )
   assert attraction_operating_hours_seconds(
      record,
      visit_date=date( 2026, 6, 20 ),
      zoo_open_seconds=9 * 3600,
      zoo_close_seconds=18 * 3600 ) == (
         DateValues.time_value_in_seconds( '11:00 AM' ),
         DateValues.time_value_in_seconds( '5:00 PM' ) )


def test_bulk_schedule_holds_attraction_until_configured_open(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         SPLASH_ISLAND,
         weekday_start='10:00 AM',
         weekday_end='4:00 PM',
         weekend_start='12:00 PM',
         weekend_end='5:00 PM' ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time == '12:00 PM'
   assert splash.end_time is not None
   assert splash.end_time <= '5:00 PM'


def test_bulk_schedule_leaves_attraction_unscheduled_when_hours_cannot_fit(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         SPLASH_ISLAND,
         weekday_start='10:00 AM',
         weekday_end='10:05 AM',
         weekend_start='12:00 PM',
         weekend_end='12:05 PM' ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time is None
   assert splash.end_time is None
   assert result.reasons
   assert result.reasons[ 0 ].code == (
      ItineraryErrorType.BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME )
   assert any(
      item.item_type == ItinerarySaveIssueItemType.ATTRACTION
      and item.name == SPLASH_ISLAND
      for item in result.reasons[ 0 ].items )


def test_bulk_schedule_does_not_place_items_past_zoo_close(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """Soft-pin late-place at close must not free-pack remaining loops after it."""
   freeze_database_today( date( 2026, 6, 20 ) )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         'Conservation Carousel',
         weekday_start='9:30 AM',
         weekday_end='6:00 PM',
         weekend_start='9:30 AM',
         weekend_end='6:00 PM' ) )

   animals = itinerary_animals_for_exhibits(
      [
         'Americas Pavilion',
         'Indo-Malaya Pavilion',
         'Indo-Malaya Outdoor',
         'Malayan Woods Pavilion',
         'Africa Savanna',
      ],
      visit_date='2026-06-20' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='3:00 PM',
      departure_time=None,
      animals=animals,
      attractions=[ 'Conservation Carousel' ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_attraction_without_animal=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   zoo_close_seconds = DateValues.time_value_in_seconds( '7:00 PM' )
   assert zoo_close_seconds is not None

   carousel = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == 'Conservation Carousel' )
   assert carousel.end_time is not None
   assert DateValues.time_value_in_seconds( carousel.end_time ) <= zoo_close_seconds

   for animal in result.itinerary.animals:
      if animal.start_time is None or animal.end_time is None:
         continue

      end_seconds = DateValues.time_value_in_seconds( animal.end_time )
      assert end_seconds is not None
      assert end_seconds <= zoo_close_seconds, (
         f'{ animal.species } ends at { animal.end_time } after zoo close' )

   for attraction in result.itinerary.attractions:
      if attraction.start_time is None or attraction.end_time is None:
         continue

      end_seconds = DateValues.time_value_in_seconds( attraction.end_time )
      assert end_seconds is not None
      assert end_seconds <= zoo_close_seconds, (
         f'{ attraction.name } ends at { attraction.end_time } after zoo close' )


def test_bulk_schedule_left_aligns_free_loops_before_soft_pin_late_place(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """Tail-reserved soft pins must not shove free loops to the end of the day."""
   freeze_database_today( date( 2026, 6, 20 ) )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         'Conservation Carousel',
         weekday_start='9:30 AM',
         weekday_end='6:00 PM',
         weekend_start='9:30 AM',
         weekend_end='6:00 PM' ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='1:00 PM',
      departure_time=None,
      animals=[ AMUR_TIGER ],
      attractions=[ 'Conservation Carousel' ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_attraction_without_animal=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   tiger = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Amur Tiger' )
   carousel = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == 'Conservation Carousel' )

   assert tiger.start_time is not None
   assert tiger.end_time is not None
   assert carousel.start_time is not None
   tiger_start = DateValues.time_value_in_seconds( tiger.start_time )
   tiger_end = DateValues.time_value_in_seconds( tiger.end_time )
   carousel_start = DateValues.time_value_in_seconds( carousel.start_time )
   morning = DateValues.time_value_in_seconds( '10:00 AM' )
   assert tiger_start is not None
   assert tiger_end is not None
   assert carousel_start is not None
   assert morning is not None
   # Contiguous from day start — free loops must not be shoved to day end.
   assert tiger_start <= morning
   assert tiger_end <= carousel_start
   # Soft pin follows the free loop without a multi-hour dead gap.
   assert carousel_start - tiger_end <= 30 * 60


def test_bulk_schedule_fills_wait_with_already_open_soft_pin(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """An already-open soft pin can fill the wait before a later-opening pin."""
   freeze_database_today( date( 2026, 6, 20 ) )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         'Zoomobile',
         weekday_start='10:00 AM',
         weekday_end='6:00 PM',
         weekend_start='10:00 AM',
         weekend_end='6:00 PM' ) )
   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         SPLASH_ISLAND,
         weekday_start='12:00 PM',
         weekday_end='4:00 PM',
         weekend_start='12:00 PM',
         weekend_end='4:00 PM' ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='10:00 AM',
      departure_time=None,
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      transportations=[
         ItineraryTransportationInput(
            name='Zoomobile',
            added_as_attraction=True ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_attraction_without_animal=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   zoomobile = next(
      transportation
      for transportation in result.itinerary.transportations
      if transportation.name == 'Zoomobile' )
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )

   assert zoomobile.start_time is not None
   assert zoomobile.end_time is not None
   assert splash.start_time is not None
   zoomobile_start = DateValues.time_value_in_seconds( zoomobile.start_time )
   splash_start = DateValues.time_value_in_seconds( splash.start_time )
   assert zoomobile_start is not None
   assert splash_start is not None
   assert zoomobile_start < splash_start
   assert zoomobile.end_time <= splash.start_time
   assert splash.start_time == '12:00 PM'
   # Right-aligned against Splash open — not left at 10:00 with a dead gap.
   # Zoomobile loop duration is 75 minutes (summer route).
   zoomobile_end = DateValues.time_value_in_seconds( zoomobile.end_time )
   assert zoomobile_end is not None
   assert splash_start - zoomobile_end <= 5 * 60
   assert zoomobile_start >= DateValues.time_value_in_seconds( '10:00 AM' )


def test_bulk_schedule_right_aligns_soft_pins_against_hard_pin_deadline(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """Face Painting should sit beside the rainforest weave, not at first open."""
   from itinerary.support import TURTLE_TALK
   from itinerary.support import guardians_talk_save_entry
   from wild_encounter_schedule_support import wire_schedule_rows

   from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator

   freeze_database_today( date( 2026, 6, 20 ) )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         'Zoomobile',
         weekday_start='10:00 AM',
         weekday_end='6:00 PM',
         weekend_start='10:00 AM',
         weekend_end='6:00 PM' ) )
   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         'Face Painting, Caricatures and Henna! - Tundra Trek',
         weekday_start='11:00 AM',
         weekday_end='4:00 PM',
         weekend_start='11:00 AM',
         weekend_end='4:00 PM' ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=TURTLE_TALK,
      location='African Rainforest Pavilion',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         '12:00',
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ),
      message=None,
   )

   rainforest = itinerary_animals_for_exhibits(
      [ 'African Rainforest Pavilion' ],
      visit_date='2026-06-20' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='10:00 AM',
      departure_time='17:00',
      animals=rainforest,
      attractions=[
         'Face Painting, Caricatures and Henna! - Tundra Trek',
      ],
      transportations=[
         ItineraryTransportationInput(
            name='Zoomobile',
            added_as_attraction=True ),
      ],
      guardians_talks=[
         guardians_talk_save_entry( TURTLE_TALK, start_time='12:00' ),
      ],
      wild_encounters=[],
      selected_exhibits=[ 'African Rainforest Pavilion' ],
      confirming_attraction_without_animal=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals(
      confirming_fixed_time_item_long_wait=True )

   assert result.success
   zoomobile = next(
      transportation
      for transportation in result.itinerary.transportations
      if transportation.name == 'Zoomobile' )
   face_painting = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name.startswith( 'Face Painting' ) )
   rainforest_scheduled = [
      animal
      for animal in result.itinerary.animals
      if animal.exhibit == 'African Rainforest Pavilion'
      and animal.start_time is not None
   ]
   assert zoomobile.end_time is not None
   assert face_painting.start_time is not None
   assert face_painting.end_time is not None
   assert rainforest_scheduled

   first_rainforest = min(
      DateValues.time_value_in_seconds( animal.start_time )
      for animal in rainforest_scheduled )
   face_end = DateValues.time_value_in_seconds( face_painting.end_time )
   zoomobile_end = DateValues.time_value_in_seconds( zoomobile.end_time )
   face_start = DateValues.time_value_in_seconds( face_painting.start_time )
   assert first_rainforest is not None
   assert face_end is not None
   assert zoomobile_end is not None
   assert face_start is not None
   assert face_start - zoomobile_end <= 5 * 60
   assert first_rainforest - face_end <= 5 * 60


def test_bulk_schedule_cascades_greenhouse_and_carousel_before_soft_pin_chain(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """Greenhouse and Carousel must not sit at open with gaps before Zoomobile.

   Inactive soft-pin opens (Carousel 9:30, Zoomobile 10:00) must not fragment
   the wait into short left-packed pockets before Face Painting / rainforest.
   """
   from itinerary.support import TURTLE_TALK
   from itinerary.support import guardians_talk_save_entry
   from wild_encounter_schedule_support import wire_schedule_rows

   from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator

   freeze_database_today( date( 2026, 6, 20 ) )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         'Conservation Carousel',
         weekday_start='9:30 AM',
         weekday_end='6:00 PM',
         weekend_start='9:30 AM',
         weekend_end='6:00 PM' ) )
   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         'Zoomobile',
         weekday_start='10:00 AM',
         weekday_end='6:00 PM',
         weekend_start='10:00 AM',
         weekend_end='6:00 PM' ) )
   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         'Face Painting, Caricatures and Henna! - Tundra Trek',
         weekday_start='11:00 AM',
         weekday_end='4:00 PM',
         weekend_start='11:00 AM',
         weekend_end='4:00 PM' ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=TURTLE_TALK,
      location='African Rainforest Pavilion',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         '12:00',
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ),
      message=None,
   )

   rainforest = itinerary_animals_for_exhibits(
      [ 'African Rainforest Pavilion' ],
      visit_date='2026-06-20' )
   americas_outdoor = itinerary_animals_for_exhibits(
      [ 'Americas Outdoor Mayan Temple Ruins' ],
      visit_date='2026-06-20' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='17:00',
      animals=[ *americas_outdoor, *rainforest ],
      attractions=[
         'Greenhouse',
         'Conservation Carousel',
         'Face Painting, Caricatures and Henna! - Tundra Trek',
      ],
      transportations=[
         ItineraryTransportationInput(
            name='Zoomobile',
            added_as_attraction=True ),
      ],
      guardians_talks=[
         guardians_talk_save_entry( TURTLE_TALK, start_time='12:00' ),
      ],
      wild_encounters=[],
      selected_exhibits=[
         'Americas Outdoor Mayan Temple Ruins',
         'African Rainforest Pavilion',
      ],
      confirming_attraction_without_animal=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals(
      confirming_fixed_time_item_long_wait=True )

   assert result.success

   def _attraction( name: str ) -> Attraction:
      return next(
         attraction
         for attraction in result.itinerary.attractions
         if attraction.name == name or attraction.name.startswith( name ) )

   def _transportation( name: str ) -> ItineraryTransportation:
      return next(
         transportation
         for transportation in result.itinerary.transportations
         if transportation.name == name )

   greenhouse = _attraction( 'Greenhouse' )
   carousel = _attraction( 'Conservation Carousel' )
   zoomobile = _transportation( 'Zoomobile' )
   face_painting = _attraction( 'Face Painting' )
   americas_scheduled = [
      animal
      for animal in result.itinerary.animals
      if animal.exhibit == 'Americas Outdoor Mayan Temple Ruins'
      and animal.start_time is not None
   ]

   assert greenhouse.end_time is not None
   assert carousel.start_time is not None
   assert carousel.end_time is not None
   assert zoomobile.start_time is not None
   assert zoomobile.end_time is not None
   assert face_painting.start_time is not None
   assert americas_scheduled

   greenhouse_end = DateValues.time_value_in_seconds( greenhouse.end_time )
   carousel_start = DateValues.time_value_in_seconds( carousel.start_time )
   carousel_end = DateValues.time_value_in_seconds( carousel.end_time )
   zoomobile_start = DateValues.time_value_in_seconds( zoomobile.start_time )
   zoomobile_end = DateValues.time_value_in_seconds( zoomobile.end_time )
   face_start = DateValues.time_value_in_seconds( face_painting.start_time )
   first_americas = min(
      DateValues.time_value_in_seconds( animal.start_time )
      for animal in americas_scheduled )
   assert greenhouse_end is not None
   assert carousel_start is not None
   assert carousel_end is not None
   assert zoomobile_start is not None
   assert zoomobile_end is not None
   assert face_start is not None
   assert first_americas is not None

   # Contiguous morning cascade — no empty pockets between free/soft attractions.
   assert carousel_start - greenhouse_end <= 5 * 60
   next_after_carousel = min( first_americas, zoomobile_start )
   assert next_after_carousel - carousel_end <= 5 * 60
   assert face_start - zoomobile_end <= 5 * 60
   # Not left at zoo open with a long dead wait before the soft-pin chain.
   # Zoomobile's 75-minute summer loop can pull the cascade slightly before 10:00.
   assert greenhouse_end >= DateValues.time_value_in_seconds( '9:45 AM' )


def test_bulk_schedule_weaves_animals_around_attraction_hours(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         KANGAROO_WALK_THRU,
         weekday_start='10:00 AM',
         weekday_end='4:00 PM',
         weekend_start='12:00 PM',
         weekend_end='4:00 PM' ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ WOMBAT, KANGAROO, AMUR_TIGER ],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   wombat = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == "Southern Hairy-Nosed Wombat" )
   kangaroo = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Western Grey Kangaroo' )
   walk_thru = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == KANGAROO_WALK_THRU )
   tiger = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Amur Tiger' )

   assert kangaroo.covered_by_talk is True
   assert kangaroo.start_time == walk_thru.start_time
   assert kangaroo.end_time == walk_thru.end_time
   assert walk_thru.start_time == '12:00 PM'
   assert walk_thru.end_time is not None
   assert walk_thru.end_time <= '4:00 PM'
   assert wombat.end_time is not None
   assert wombat.end_time <= walk_thru.start_time
   assert tiger.start_time is not None
   assert walk_thru.end_time <= tiger.start_time
