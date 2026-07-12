from __future__ import annotations

from typing import Any

from http_support import make_handler
from http_support import response_json
from http_support import StubZooControllers
import pytest

import api.server as server


GUARDIANS_TALK_SCHEDULE_BODY = {
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
   'message': 'Schedule.',
}


@pytest.mark.parametrize(
   'path, expected_method',
   [
      (
         '/replace-guardians-talk-schedule-overlaps',
         'replace_guardians_talk_schedule_overlaps'
      ),
      (
         '/trim-guardians-talk-schedule-overlaps',
         'trim_guardians_talk_schedule_overlaps'
      ),
   ]
)
def test_guardians_talk_schedule_overlap_resolution_maps_payload(
      stub_database: type[ StubZooControllers ],
      path: str,
      expected_method: str ) -> None:
   handler = make_handler( path, GUARDIANS_TALK_SCHEDULE_BODY )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         expected_method,
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'start_date': '2026-06-01',
            'end_date': '2026-06-30',
            'schedule_rows': GUARDIANS_TALK_SCHEDULE_BODY[ 'scheduleRows' ],
            'message': 'Schedule.',
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'talk' ] == 'African Lion'
   assert result[ 'location' ] == 'Africa Savanna'
   assert result[ 'startDate' ] == '2026-06-01'
   assert result[ 'endDate' ] == '2026-06-30'


def test_guardians_talk_schedule_overlap_failure_returns_error_type(
      stub_database: type[ StubZooControllers ] ) -> None:
   StubZooControllers.default_success = False
   handler = make_handler(
      '/set-guardians-talk-schedule',
      GUARDIANS_TALK_SCHEDULE_BODY )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'errorType' ] == 'overlappingSchedule'
