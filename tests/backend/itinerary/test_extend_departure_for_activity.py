from __future__ import annotations

from api.itinerary.scheduling.extend_departure_for_activity import arrival_time_covering_schedule_starts
from api.itinerary.scheduling.extend_departure_for_activity import departure_time_covering_schedule_ends


def test_arrival_time_covering_leaves_unset_arrival_unset() -> None:
   assert arrival_time_covering_schedule_starts(
      None,
      [ '11:00', '10:00' ],
   ) is None


def test_arrival_time_covering_keeps_earlier_existing_arrival() -> None:
   assert arrival_time_covering_schedule_starts(
      '09:00',
      [ '10:00', '11:00' ],
   ) == '09:00'


def test_arrival_time_covering_pulls_existing_arrival_earlier() -> None:
   assert arrival_time_covering_schedule_starts(
      '11:00',
      [ '10:00' ],
   ) == '10:00'


def test_arrival_time_covering_returns_existing_when_no_starts() -> None:
   assert arrival_time_covering_schedule_starts( '09:00', [] ) == '09:00'


def test_departure_time_covering_leaves_unset_departure_unset() -> None:
   assert departure_time_covering_schedule_ends(
      None,
      [ '10:00', '11:30' ],
   ) is None


def test_departure_time_covering_keeps_later_existing_departure() -> None:
   assert departure_time_covering_schedule_ends(
      '17:00',
      [ '10:00', '11:00' ],
   ) == '17:00'


def test_departure_time_covering_pushes_existing_departure_later() -> None:
   assert departure_time_covering_schedule_ends(
      '11:00',
      [ '11:30' ],
   ) == '11:30'


def test_departure_time_covering_returns_existing_when_no_ends() -> None:
   assert departure_time_covering_schedule_ends( '17:00', [] ) == '17:00'
