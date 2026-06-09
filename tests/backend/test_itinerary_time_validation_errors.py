from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.data_access.itinerary import fetch_itinerary_date
from api.itinerary.logic.itinerary_arrival_time_validation import arrival_time_is_valid_for_zoo_hours
from api.itinerary.logic.itinerary_departure_time_validation import departure_time_is_valid_for_zoo_hours
from api.itinerary.logic.itinerary_schedule_time_order_validation import departure_follows_arrival
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from api.zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record
from conftest import DbControllers

GUARDIANS_TALK = 'African Lion'
WILD_ENCOUNTER = 'African Rainforest'
CAROUSEL = 'Conservation Carousel'
LION_KEY = 'African Lion||Africa Savanna'
CHEETAH_KEY = 'Cheetah||Africa Savanna'


def _guardians_talk_save_entry(
      name: str,
      *,
      start_time: str,
      end_time: str ) -> dict[ str, str ]:
   return {
      'name': name,
      'start_time': start_time,
      'end_time': end_time,
   }


def _set_wild_encounter_schedule( *, encounter_time: str ) -> None:
   assert WildEncounterController.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time=encounter_time,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None,
   )


def test_arrival_time_is_valid_for_zoo_hours(
      db: DbControllers ) -> None:
   conn = db.conn

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   zoo_hours_record = fetch_zoo_hours_record( conn, fetch_itinerary_date( conn ) )

   assert arrival_time_is_valid_for_zoo_hours(
      '09:00',
      zoo_hours_record,
      departure_time='17:00' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert arrival_time_is_valid_for_zoo_hours(
      '17:00',
      zoo_hours_record,
      departure_time='17:00' ) == ItineraryErrorType.TIME_ORDER_INVALID
   assert arrival_time_is_valid_for_zoo_hours(
      '10:00',
      zoo_hours_record,
      departure_time='17:00' ) == ItineraryErrorType.SUCCESS
   assert arrival_time_is_valid_for_zoo_hours(
      '10:00',
      zoo_hours_record,
      departure_time=None ) == ItineraryErrorType.SUCCESS


def test_departure_follows_arrival_when_other_time_is_unset() -> None:
   assert departure_follows_arrival( '10:00', None )
   assert departure_follows_arrival( None, '17:00' )


def test_departure_time_is_valid_for_zoo_hours(
      db: DbControllers ) -> None:
   conn = db.conn

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   zoo_hours_record = fetch_zoo_hours_record( conn, fetch_itinerary_date( conn ) )

   assert departure_time_is_valid_for_zoo_hours(
      '09:00',
      zoo_hours_record,
      arrival_time='09:30' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert departure_time_is_valid_for_zoo_hours(
      '09:30',
      zoo_hours_record,
      arrival_time='09:30' ) == ItineraryErrorType.TIME_ORDER_INVALID
   assert departure_time_is_valid_for_zoo_hours(
      '18:00',
      zoo_hours_record,
      arrival_time='09:30' ) == ItineraryErrorType.SUCCESS
   assert departure_time_is_valid_for_zoo_hours(
      '18:00',
      zoo_hours_record,
      arrival_time=None ) == ItineraryErrorType.SUCCESS


def test_set_arrival_time_returns_validation_error_types(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.set_arrival_time( '09:00' ).status == (
      ItineraryErrorType.TIME_OUT_OF_BOUNDS )
   assert ItineraryController.set_arrival_time( '17:00' ).status == (
      ItineraryErrorType.TIME_ORDER_INVALID )


def test_set_arrival_time_succeeds_when_departure_is_unset(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success
   assert ItineraryController.set_departure_time( None ).success

   assert ItineraryController.set_arrival_time( '10:15' ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '10:15'
   assert itinerary.departure_time is None


def test_set_arrival_time_unschedules_items_before_arrival(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='10:00',
   ).success
   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='10:30',
   ).success
   assert ItineraryController.schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time='10:10',
   ).success

   _set_wild_encounter_schedule( encounter_time='09:45' )

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         _guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='10:00',
            end_time='10:10',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_wild_encounter_unschedule=True,
   ).success

   result = ItineraryController.set_arrival_time( '10:15' )
   itinerary = ItineraryController.get_itinerary()

   assert result.success
   assert result.itinerary is not None
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', None, None ),
      ( 'Cheetah', '10:30', '10:35' ),
   ]
   assert [
      ( attraction.name, attraction.start_time, attraction.end_time )
      for attraction in itinerary.attractions
   ] == [
      ( CAROUSEL, None, None ),
   ]
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []


def test_set_arrival_time_unschedules_generic_event_before_arrival(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='',
   ).success

   result = ItineraryController.set_arrival_time( '10:15' )
   itinerary = ItineraryController.get_itinerary()

   assert result.success
   assert itinerary.events == []


def test_set_departure_time_unschedules_items_after_departure(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='15:45',
   ).success
   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='16:30',
   ).success
   assert ItineraryController.schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time='15:54',
   ).success

   _set_wild_encounter_schedule( encounter_time='16:30' )

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         _guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='16:30',
            end_time='16:45',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_wild_encounter_unschedule=True,
   ).success

   result = ItineraryController.set_departure_time( '16:15' )
   itinerary = ItineraryController.get_itinerary()

   assert result.success
   assert result.itinerary is not None
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', '15:45', '15:53' ),
      ( 'Cheetah', None, None ),
   ]
   assert itinerary.attractions[ 0 ].name == CAROUSEL
   assert itinerary.attractions[ 0 ].start_time is not None
   assert itinerary.attractions[ 0 ].end_time is not None
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []


def test_set_departure_time_unschedules_generic_event_after_departure(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='',
      start_time='16:00',
   ).success

   result = ItineraryController.set_departure_time( '16:15' )
   itinerary = ItineraryController.get_itinerary()

   assert result.success
   assert itinerary.events == []


def test_set_itinerary_rejects_invalid_departure_on_date_change_without_adjustment(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryController.set_itinerary(
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

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.date == '2026-06-20'
   assert itinerary.departure_time == '18:30'


def test_date_change_with_adjusted_arrival_unschedules_all_item_types_before_arrival(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='09:20',
   ).success
   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='10:30',
   ).success
   assert ItineraryController.schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time='10:10',
   ).success

   _set_wild_encounter_schedule( encounter_time='09:20' )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         _guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='09:20',
            end_time='09:30',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_early_admission=True,
      confirming_wild_encounter_unschedule=True,
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='',
   ).success

   result = ItineraryController.set_itinerary(
      date='2026-06-22',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         _guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='09:20',
            end_time='09:30',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_wild_encounter_unschedule=True,
   )

   itinerary = result.itinerary

   assert result.success
   assert itinerary is not None
   assert itinerary.arrival_time == '09:30'
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', None, None ),
      ( 'Cheetah', '10:30', '10:35' ),
   ]
   assert itinerary.attractions[ 0 ].name == CAROUSEL
   assert itinerary.attractions[ 0 ].start_time == '10:10'
   assert itinerary.attractions[ 0 ].end_time is not None
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []
   assert itinerary.events == []


def test_date_change_with_adjusted_departure_unschedules_all_item_types_after_departure(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='15:45',
   ).success
   assert ItineraryController.schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time='15:54',
   ).success
   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='18:15',
   ).success

   _set_wild_encounter_schedule( encounter_time='18:15' )

   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         _guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='18:15',
            end_time='18:30',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_wild_encounter_unschedule=True,
   ).success

   result = ItineraryController.set_itinerary(
      date='2026-06-22',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'Cheetah',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         _guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='18:15',
            end_time='18:30',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_wild_encounter_unschedule=True,
   )

   itinerary = result.itinerary

   assert result.success
   assert itinerary is not None
   assert itinerary.departure_time == '18:00'
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', '15:45', '15:53' ),
      ( 'Cheetah', None, None ),
   ]
   assert itinerary.attractions[ 0 ].name == CAROUSEL
   assert itinerary.attractions[ 0 ].start_time is not None
   assert itinerary.attractions[ 0 ].end_time is not None
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []
