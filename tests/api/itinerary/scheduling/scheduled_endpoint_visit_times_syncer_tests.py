from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer import ScheduledEndpointVisitTimesSyncer
from api.models import Animal
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import ItineraryTransportation
from api.models import WildEncounter


VISIT_DATE = '2026-06-15'
ENTRANCE_TRAVEL_SECONDS = 10 * 60
ZOOMOBILE = 'Zoomobile'


def _fully_scheduled_lion_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=None,
      departure_time=None )


def _talk_only_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[
         GuardiansTalk(
            name='Turtle Talk',
            location='Americas Pavilion',
            x_coord=0,
            y_coord=0,
            start_time='10:00 AM',
            end_time='10:15 AM' ),
      ],
      wild_encounters=[],
      events=[],
      arrival_time=None,
      departure_time=None )


def _wild_encounter_only_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[
         WildEncounter(
            name='African Rainforest',
            meeting_spot='Rainforest Gate',
            link='african-rainforest',
            x_coord=0,
            y_coord=0,
            start_time='3:30 PM',
            end_time='4:15 PM' ),
      ],
      events=[],
      arrival_time=None,
      departure_time=None )


def _two_animal_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:08 AM' ),
         Animal(
            species='Cheetah',
            exhibit='Africa Savanna',
            start_time='11:00 AM',
            end_time='11:08 AM' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=None,
      departure_time=None )


def _lion_at_eleven_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='11:00 AM',
            end_time='11:08 AM' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )


def _partially_scheduled_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='9:23 AM',
            end_time='9:31 AM' ),
         Animal(
            species='Cheetah',
            exhibit='Africa Savanna' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:15 AM',
      departure_time='9:35 AM' )


def _morning_rescheduled_lion_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='9:40 AM',
            end_time='9:48 AM' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='6:00 PM',
      departure_time='6:00 PM' )


@pytest.fixture
def syncer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_IsFullyScheduled_TestUnscheduledAnimal_ExpectFalse() -> None:
   itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=None,
      departure_time=None )

   assert not ScheduledEndpointVisitTimesSyncer.is_fully_scheduled( itinerary )


def Test_IsFullyScheduled_TestFullyScheduledAnimal_ExpectTrue() -> None:
   assert ScheduledEndpointVisitTimesSyncer.is_fully_scheduled(
      _fully_scheduled_lion_itinerary() )


def Test_IsFullyScheduled_TestPartialSchedule_ExpectFalse() -> None:
   assert not ScheduledEndpointVisitTimesSyncer.is_fully_scheduled(
      _partially_scheduled_itinerary() )


def Test_IsFullyScheduled_TestEmptyDay_ExpectFalse() -> None:
   itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=None,
      departure_time=None )

   assert not ScheduledEndpointVisitTimesSyncer.is_fully_scheduled( itinerary )


def Test_SeedIfComplete_TestUnscheduledAnimal_ExpectNoUpdate(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda *args, **kwargs: pytest.fail( 'arrival should not be updated' ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda *args, **kwargs: pytest.fail( 'departure should not be updated' ) )

   itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=None,
      departure_time=None )

   ScheduledEndpointVisitTimesSyncer.seed_if_complete( syncer_conn, itinerary )


def Test_SeedIfComplete_TestPartialSchedule_ExpectStaleDeparturePreserved(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda *args, **kwargs: pytest.fail( 'arrival should not be updated' ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda *args, **kwargs: pytest.fail( 'departure should not be updated' ) )

   ScheduledEndpointVisitTimesSyncer.seed_if_complete(
      syncer_conn,
      _partially_scheduled_itinerary() )


def Test_SeedIfComplete_TestFullyScheduledAnimal_ExpectArrivalAndDeparture(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   updated: dict[ str, str | None ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda conn, arrival_time: updated.__setitem__( 'arrival_time', arrival_time ) or True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda conn, departure_time: updated.__setitem__( 'departure_time', departure_time ) or True )

   ScheduledEndpointVisitTimesSyncer.seed_if_complete(
      syncer_conn,
      _fully_scheduled_lion_itinerary() )

   assert updated == {
      'arrival_time': '9:50 AM',
      'departure_time': '10:18 AM',
   }


def Test_SeedIfComplete_TestTalkOnlyItinerary_ExpectArrivalAndDeparture(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   updated: dict[ str, str | None ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda conn, arrival_time: updated.__setitem__( 'arrival_time', arrival_time ) or True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda conn, departure_time: updated.__setitem__( 'departure_time', departure_time ) or True )

   ScheduledEndpointVisitTimesSyncer.seed_if_complete(
      syncer_conn,
      _talk_only_itinerary() )

   assert updated == {
      'arrival_time': '9:50 AM',
      'departure_time': '10:25 AM',
   }


def Test_ClearIfBecameIncomplete_TestLosesSchedule_ExpectTimesCleared(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   cleared: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda conn, arrival_time: cleared.append( 'arrival' ) or True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda conn, departure_time: cleared.append( 'departure' ) or True )

   previous_itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:50 AM',
      departure_time='10:18 AM' )
   current_itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:50 AM',
      departure_time='10:18 AM' )

   ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete(
      syncer_conn,
      previous_itinerary=previous_itinerary,
      current_itinerary=current_itinerary )

   assert cleared == [ 'arrival', 'departure' ]


def Test_SeedIfComplete_TestWildEncounterOnly_ExpectArrivalAndDeparture(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   updated: dict[ str, str | None ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda conn, arrival_time: updated.__setitem__( 'arrival_time', arrival_time ) or True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda conn, departure_time: updated.__setitem__( 'departure_time', departure_time ) or True )

   ScheduledEndpointVisitTimesSyncer.seed_if_complete(
      syncer_conn,
      _wild_encounter_only_itinerary() )

   assert updated == {
      'arrival_time': '3:20 PM',
      'departure_time': '4:25 PM',
   }


def Test_SeedIfComplete_TestTwoAnimals_ExpectDepartureFromLatestEnd(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   updated: dict[ str, str | None ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda conn, arrival_time: updated.__setitem__( 'arrival_time', arrival_time ) or True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda conn, departure_time: updated.__setitem__( 'departure_time', departure_time ) or True )

   ScheduledEndpointVisitTimesSyncer.seed_if_complete(
      syncer_conn,
      _two_animal_itinerary() )

   assert updated == {
      'arrival_time': '9:50 AM',
      'departure_time': '11:18 AM',
   }


def Test_SeedIfComplete_TestLionAtEleven_ExpectArrivalFromEarliestStart(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   updated: dict[ str, str | None ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda conn, arrival_time: updated.__setitem__( 'arrival_time', arrival_time ) or True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda conn, departure_time: updated.__setitem__( 'departure_time', departure_time ) or True )

   ScheduledEndpointVisitTimesSyncer.seed_if_complete(
      syncer_conn,
      _lion_at_eleven_itinerary() )

   assert updated[ 'arrival_time' ] == '10:50 AM'
   assert updated[ 'departure_time' ] == '11:18 AM'


def Test_SeedIfComplete_TestMorningRescheduledLion_ExpectDepartureFromEndPlusTravel(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   updated: dict[ str, str | None ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda conn, arrival_time: updated.__setitem__( 'arrival_time', arrival_time ) or True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda conn, departure_time: updated.__setitem__( 'departure_time', departure_time ) or True )

   ScheduledEndpointVisitTimesSyncer.seed_if_complete(
      syncer_conn,
      _morning_rescheduled_lion_itinerary() )

   assert updated == {
      'arrival_time': '9:30 AM',
      'departure_time': '9:58 AM',
   }


def Test_SyncIfComplete_TestGuestDepartureSet_ExpectDepartureFromLatestAnimalEnd(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   updated: dict[ str, str | None ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_earliest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_latest_item',
      lambda itinerary: ENTRANCE_TRAVEL_SECONDS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda conn, arrival_time: updated.__setitem__( 'arrival_time', arrival_time ) or True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda conn, departure_time: updated.__setitem__( 'departure_time', departure_time ) or True )

   itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='9:38 AM',
            end_time='9:46 AM' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )

   ScheduledEndpointVisitTimesSyncer.sync_if_complete( syncer_conn, itinerary )

   assert updated == {
      'arrival_time': '9:28 AM',
      'departure_time': '9:56 AM',
   }


def Test_ClearIfBecameIncomplete_TestZoomobileUnscheduledAnimalRemains_ExpectVisitTimesCleared(
      syncer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   cleared: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda conn, arrival_time: cleared.append( 'arrival' ) or True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda conn, departure_time: cleared.append( 'departure' ) or True )

   previous_itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
      attractions=[],
      transportations=[
         ItineraryTransportation(
            name=ZOOMOBILE,
            added_as_attraction=True,
            start_time='11:00 AM',
            end_time='11:30 AM' ),
      ],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:50 AM',
      departure_time='11:40 AM' )
   current_itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
      attractions=[],
      transportations=[
         ItineraryTransportation(
            name=ZOOMOBILE,
            added_as_attraction=True ),
      ],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:50 AM',
      departure_time='11:40 AM' )

   ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete(
      syncer_conn,
      previous_itinerary=previous_itinerary,
      current_itinerary=current_itinerary )

   assert cleared == [ 'arrival', 'departure' ]
   assert current_itinerary.animals[ 0 ].start_time == '10:00 AM'
