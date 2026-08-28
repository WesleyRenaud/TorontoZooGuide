from __future__ import annotations

from itinerary.support import CAROUSEL, CHEETAH_ITINERARY_ENTRY, CHEETAH_KEY, entrance_travel_seconds_to_animal, expected_departure_time_for_itinerary, GUARDIANS_TALK, guardians_talk_save_entry, LION_ITINERARY_ENTRY, LION_KEY, schedule_itinerary_item, schedule_time_after_seconds, schedule_time_before_seconds, set_wild_encounter_schedule, WILD_ENCOUNTER, wild_encounter_key

from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver

LION_TRAVEL_SECONDS = entrance_travel_seconds_to_animal(
   species='African Lion',
   exhibit='Africa Savanna',
)
LION_START_AFTER_915 = schedule_time_after_seconds( '9:15 AM', LION_TRAVEL_SECONDS )
LION_START_AFTER_930 = schedule_time_after_seconds( '9:30 AM', LION_TRAVEL_SECONDS )
LION_CHEETAH_TRAVEL_SECONDS = WalkTravelTimeCalculator.seconds_between_nodes(
   WalkGraphProvider.fetch(),
   ViewingSpotWalkNodeIdResolver.resolve( 'African Lion', 'Africa Savanna', None ),
   ViewingSpotWalkNodeIdResolver.resolve( 'Cheetah', 'Africa Savanna', None ),
)
EXPECTED_REPACKED_LION_END = schedule_time_after_seconds( LION_START_AFTER_930, 8 * 60 )
EXPECTED_REPACKED_CHEETAH_START = schedule_time_after_seconds(
   EXPECTED_REPACKED_LION_END,
   LION_CHEETAH_TRAVEL_SECONDS )
EXPECTED_REPACKED_CHEETAH_END = schedule_time_after_seconds(
   EXPECTED_REPACKED_CHEETAH_START,
   5 * 60 )
LION_END_AFTER_915 = schedule_time_after_seconds( LION_START_AFTER_915, 8 * 60 )
CAROUSEL_AFTER_LION_AFTERNOON = schedule_time_after_seconds(
   schedule_time_after_seconds( '3:45 PM', 8 * 60 ),
   WalkTravelTimeCalculator.seconds_between_nodes(
      WalkGraphProvider.fetch(),
      ViewingSpotWalkNodeIdResolver.resolve( 'African Lion', 'Africa Savanna', None ),
      ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction( CAROUSEL ),
   ),
)

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from conftest import DbControllers


def test_set_itinerary_rejects_invalid_departure_on_date_change_without_adjustment(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:30',
      departure_time='19:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.TIME_OUT_OF_BOUNDS

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.date == '2026-06-20'
   assert itinerary.departure_time == '6:30 PM'


def test_date_change_with_adjusted_arrival_reschedules_animals_and_clears_guest_schedules(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time=LION_START_AFTER_915,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='10:30',
   ).success
   assert schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time='11:00',
   ).success

   set_wild_encounter_schedule( encounter_time='09:20' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='09:20',
            end_time='09:30',
         ),
      ],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER, start_time='09:20' ) ],
      confirming_early_admission=True,
      confirming_wild_encounter_unschedule=True,
   ).success

   assert schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='',
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='09:20',
            end_time='09:30',
         ),
      ],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER, start_time='09:20' ) ],
      confirming_wild_encounter_unschedule=True,
   )

   itinerary = result.itinerary

   assert result.success
   assert itinerary is not None
   assert itinerary.arrival_time == schedule_time_before_seconds(
      LION_START_AFTER_915,
      LION_TRAVEL_SECONDS )
   assert itinerary.departure_time == expected_departure_time_for_itinerary(
      itinerary )
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', LION_START_AFTER_915, LION_END_AFTER_915 ),
      ( 'Cheetah', '10:30 AM', '10:35 AM' ),
   ]
   assert itinerary.attractions[ 0 ].name == CAROUSEL
   assert itinerary.attractions[ 0 ].start_time is not None
   assert itinerary.attractions[ 0 ].end_time is not None
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []


def test_date_change_with_adjusted_arrival_keeps_stale_departure_when_incomplete(
      db: DbControllers ) -> None:
   """Past-date recovery clamps arrival; incomplete itineraries keep stale departure."""
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:15',
      departure_time='09:35',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
      confirming_short_visit=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time=LION_START_AFTER_915,
   ).success

   before = ItineraryCoordinator.get_itinerary()
   assert before.departure_time == LION_END_AFTER_915
   assert before.animals[ 0 ].species == 'African Lion'
   assert before.animals[ 0 ].end_time is not None
   assert DateValues.time_value_in_seconds( before.animals[ 0 ].end_time ) <= (
      DateValues.time_value_in_seconds( before.departure_time ) or 0 )
   assert before.animals[ 1 ].species == 'Cheetah'
   assert before.animals[ 1 ].start_time is None

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:15',
      departure_time='09:35',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_short_visit=True,
   )

   itinerary = result.itinerary

   assert result.success
   assert itinerary is not None
   assert itinerary.arrival_time == '9:30 AM'

   lion = next(
      animal for animal in itinerary.animals if animal.species == 'African Lion' )
   cheetah = next(
      animal for animal in itinerary.animals if animal.species == 'Cheetah' )

   assert lion.start_time is not None
   assert lion.end_time is not None
   assert cheetah.start_time is None

   departure_seconds = DateValues.time_value_in_seconds( itinerary.departure_time )
   lion_end_seconds = DateValues.time_value_in_seconds( lion.end_time )
   stale_departure_seconds = DateValues.time_value_in_seconds( '9:35 AM' )

   assert lion_end_seconds is not None
   assert stale_departure_seconds is not None
   assert lion_end_seconds >= stale_departure_seconds
   assert departure_seconds == stale_departure_seconds


def test_date_change_with_adjusted_departure_reschedules_animals_and_clears_guest_schedules(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='15:45',
   ).success
   assert schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time=CAROUSEL_AFTER_LION_AFTERNOON,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='18:15',
   ).success

   set_wild_encounter_schedule( encounter_time='18:15' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='18:15',
            end_time='18:30',
         ),
      ],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER, start_time='18:15' ) ],
      confirming_wild_encounter_unschedule=True,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:30',
      departure_time='18:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='18:15',
            end_time='18:30',
         ),
      ],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER, start_time='18:15' ) ],
      confirming_wild_encounter_unschedule=True,
   )

   itinerary = result.itinerary

   assert result.success
   assert itinerary is not None
   assert itinerary.arrival_time == '9:30 AM'
   assert itinerary.departure_time == expected_departure_time_for_itinerary(
      itinerary )
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', '10:01 AM', '10:09 AM' ),
      ( 'Cheetah', '10:11 AM', '10:16 AM' ),
   ]
   assert itinerary.attractions[ 0 ].name == CAROUSEL
   assert itinerary.attractions[ 0 ].start_time is not None
   assert itinerary.attractions[ 0 ].end_time is not None
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []
