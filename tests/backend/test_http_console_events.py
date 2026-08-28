from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_failure, assert_console_mutation_success
from http_support import make_handler
from http_support import response_json
from http_support import StubZooControllers
import pytest

import api.http_request_handler as server

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
            'scheduleRows': [
               {
                  'time': '10:00',
                  'monday': True,
                  'tuesday': False,
                  'wednesday': False,
                  'thursday': False,
                  'friday': False,
                  'saturday': False,
                  'sunday': False,
               },
               {
                  'time': '11:00',
                  'monday': False,
                  'tuesday': False,
                  'wednesday': True,
                  'thursday': False,
                  'friday': False,
                  'saturday': False,
                  'sunday': False,
               },
               {
                  'time': '12:00',
                  'monday': False,
                  'tuesday': False,
                  'wednesday': False,
                  'thursday': False,
                  'friday': True,
                  'saturday': False,
                  'sunday': False,
               },
            ],
            'message': 'Schedule.'
         },
         (
            'set_guardians_talk_schedule',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'schedule_rows': [
                  {
                     'time': '10:00',
                     'monday': True,
                     'tuesday': False,
                     'wednesday': False,
                     'thursday': False,
                     'friday': False,
                     'saturday': False,
                     'sunday': False,
                  },
                  {
                     'time': '11:00',
                     'monday': False,
                     'tuesday': False,
                     'wednesday': True,
                     'thursday': False,
                     'friday': False,
                     'saturday': False,
                     'sunday': False,
                  },
                  {
                     'time': '12:00',
                     'monday': False,
                     'tuesday': False,
                     'wednesday': False,
                     'thursday': False,
                     'friday': True,
                     'saturday': False,
                     'sunday': False,
                  },
               ],
               'message': 'Schedule.'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
         }
      ),
      (
         '/end-guardians-talk-schedule',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'endDate': '2026-06-30',
            'times': [ '10:00' ],
         },
         (
            'end_guardians_talk_schedule',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'schedule_end_date': '2026-06-30',
               'talk_times': [ '10:00' ],
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
            'times': [ '10:00 AM' ],
         },
         (
            'cancel_guardians_talk_occurrence',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'date': '2026-06-15',
               'talk_times': [ '10:00 AM' ],
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'date': '2026-06-15',
            'times': [ '10:00 AM' ],
         }
      ),
      (
         '/add-guardians-talk-occurrence',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'date': '2026-06-20',
            'times': [ '3:00 PM' ],
         },
         (
            'add_guardians_talk_occurrence',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'date': '2026-06-20',
               'talk_times': [ '3:00 PM' ],
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'date': '2026-06-20',
            'times': [ '3:00 PM' ],
         }
      ),
      (
         '/set-wild-encounter-schedule',
         {
            'wildEncounter': 'African Rainforest',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'scheduleRows': [
               {
                  'time': '2:00 PM',
                  'monday': True,
                  'tuesday': False,
                  'wednesday': True,
                  'thursday': False,
                  'friday': True,
                  'saturday': False,
                  'sunday': True,
               },
               {
                  'time': '3:30 PM',
                  'monday': False,
                  'tuesday': True,
                  'wednesday': False,
                  'thursday': False,
                  'friday': False,
                  'saturday': True,
                  'sunday': False,
               },
            ],
            'message': 'Schedule.'
         },
         (
            'set_wild_encounter_schedule',
            {
               'wild_encounter_name': 'African Rainforest',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Schedule.',
               'schedule_rows': [
                  {
                     'time': '2:00 PM',
                     'monday': True,
                     'tuesday': False,
                     'wednesday': True,
                     'thursday': False,
                     'friday': True,
                     'saturday': False,
                     'sunday': True,
                  },
                  {
                     'time': '3:30 PM',
                     'monday': False,
                     'tuesday': True,
                     'wednesday': False,
                     'thursday': False,
                     'friday': False,
                     'saturday': True,
                     'sunday': False,
                  },
               ],
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
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
   'path, body, expected_api_error_type, expected_api_error_params',
   [
      (
         '/cancel-wild-encounter-occurrence',
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'times': [ '2:00 PM' ],
         },
         'couldNotCancelWildEncounterOccurrence',
         {
            'name': 'African Rainforest',
            'date': '2026-06-15',
         },
      ),
   ]
)
def test_console_mutation_returns_error_when_database_returns_false(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_api_error_type: str,
      expected_api_error_params: dict[ str, Any ] ) -> None:
   assert_console_mutation_failure(
      path,
      body,
      expected_api_error_type,
      expected_api_error_params )


WILD_ENCOUNTER_SCHEDULE_BODY = {
   'wildEncounter': 'African Rainforest',
   'startDate': '2026-06-01',
   'endDate': '2026-06-30',
   'scheduleRows': [
      {
         'time': '2:00 PM',
         'monday': True,
         'tuesday': False,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
   ],
   'message': 'Schedule.',
}


@pytest.mark.parametrize(
   'path, expected_method',
   [
      (
         '/replace-wild-encounter-schedule-overlaps',
         'replace_wild_encounter_schedule_overlaps'
      ),
      (
         '/trim-wild-encounter-schedule-overlaps',
         'trim_wild_encounter_schedule_overlaps'
      ),
   ]
)
def test_wild_encounter_schedule_overlap_resolution_maps_payload(
      stub_database: type[ StubZooControllers ],
      path: str,
      expected_method: str ) -> None:
   handler = make_handler( path, WILD_ENCOUNTER_SCHEDULE_BODY )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         expected_method,
         {
            'wild_encounter_name': 'African Rainforest',
            'start_date': '2026-06-01',
            'end_date': '2026-06-30',
            'message': 'Schedule.',
            'schedule_rows': WILD_ENCOUNTER_SCHEDULE_BODY[ 'scheduleRows' ],
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'wildEncounter' ] == 'African Rainforest'
   assert result[ 'startDate' ] == '2026-06-01'
   assert result[ 'endDate' ] == '2026-06-30'


def test_wild_encounter_schedule_overlap_failure_returns_error_type(
      stub_database: type[ StubZooControllers ] ) -> None:
   StubZooControllers.default_success = False
   handler = make_handler(
      '/set-wild-encounter-schedule',
      WILD_ENCOUNTER_SCHEDULE_BODY )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'errorType' ] == 'overlappingSchedule'
