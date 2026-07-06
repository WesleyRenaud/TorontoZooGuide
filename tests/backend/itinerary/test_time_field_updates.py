from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import wild_encounter_key
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def test_set_itinerary_arrival_and_departure_time_updates_only_requested_field(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.set_arrival_time( '10:15 AM' ).success
   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time == '10:15 AM'
   assert itinerary.departure_time == '5:00 PM'

   assert ItineraryCoordinator.set_arrival_time( None ).success
   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time is None
   assert itinerary.departure_time == '5:00 PM'

   assert ItineraryCoordinator.set_arrival_time( '10:15 AM' ).success
   assert ItineraryCoordinator.set_departure_time( None ).success
   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time == '10:15 AM'
   assert itinerary.departure_time is None


def test_set_itinerary_normalizes_display_format_schedule_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Grizzly Bear',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '1:00 PM' ),
      message=None
   )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( 'Grizzly Bear', start_time='13:00' ) ],
   ).success

   encounter_schedule = db.conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'Grizzly Bear';
      """ ).fetchone()

   assert dict( encounter_schedule ) == {
      'START_TIME': '1:00 PM',
      'END_TIME': '1:45 PM',
   }
