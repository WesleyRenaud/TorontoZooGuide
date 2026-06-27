from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_failure, assert_console_mutation_success
from http_support import StubZooControllers
import pytest

@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-guardians-talk-schedule',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'mondayTime': '10:00',
            'tuesdayTime': None,
            'wednesdayTime': '11:00',
            'thursdayTime': None,
            'fridayTime': '12:00',
            'saturdayTime': None,
            'sundayTime': None,
            'message': 'Schedule.'
         },
         (
            'set_guardians_talk_schedule',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'monday_time': '10:00',
               'tuesday_time': None,
               'wednesday_time': '11:00',
               'thursday_time': None,
               'friday_time': '12:00',
               'saturday_time': None,
               'sunday_time': None,
               'message': 'Schedule.'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'mondayTime': '10:00',
            'wednesdayTime': '11:00',
            'fridayTime': '12:00'
         }
      ),
      (
         '/end-guardians-talk-schedule',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'endDate': '2026-06-30'
         },
         (
            'end_guardians_talk_schedule',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'schedule_end_date': '2026-06-30'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/cancel-guardians-talk-occurrence',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'date': '2026-06-15',
            'time': '10:00 AM'
         },
         (
            'cancel_guardians_talk_occurrence',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'date': '2026-06-15',
               'time': '10:00 AM'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'date': '2026-06-15',
            'time': '10:00 AM'
         }
      ),
      (
         '/set-wild-encounter-schedule',
         {
            'wildEncounter': 'African Rainforest',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'times': [ '14:00', '15:30' ],
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'message': 'Schedule.'
         },
         (
            'set_wild_encounter_schedule',
            {
               'wild_encounter_name': 'African Rainforest',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'encounter_times': [ '14:00', '15:30' ],
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'message': 'Schedule.'
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'times': [ '14:00', '15:30' ]
         }
      ),
      (
         '/end-wild-encounter-schedule',
         {
            'wildEncounter': 'African Rainforest',
            'endDate': '2026-06-30',
            'times': [ '14:00' ],
         },
         (
            'end_wild_encounter_schedule',
            {
               'wild_encounter_name': 'African Rainforest',
               'schedule_end_date': '2026-06-30',
               'encounter_times': [ '14:00' ],
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'endDate': '2026-06-30',
            'times': [ '14:00' ],
         }
      ),
      (
         '/cancel-wild-encounter-occurrence',
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'times': [ '2:00 PM' ],
         },
         (
            'cancel_wild_encounter_occurrence',
            {
               'wild_encounter_name': 'African Rainforest',
               'date': '2026-06-15',
               'encounter_times': [ '2:00 PM' ],
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'times': [ '2:00 PM' ],
         }
      ),
   ]
)
def test_console_mutation_maps_payload_and_success_response(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_call: tuple[ str, dict[ str, Any ] ],
      response_subset: dict[ str, Any ] ) -> None:
   assert_console_mutation_success(
      path,
      body,
      expected_call,
      response_subset )

@pytest.mark.parametrize(
   'path, body, expected_error',
   [
      (
         '/cancel-wild-encounter-occurrence',
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'times': [ '2:00 PM' ],
         },
         'Could not cancel "African Rainforest" on 2026-06-15.'
      ),
   ]
)
def test_console_mutation_returns_error_when_database_returns_false(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_error: str ) -> None:
   assert_console_mutation_failure( path, body, expected_error )

