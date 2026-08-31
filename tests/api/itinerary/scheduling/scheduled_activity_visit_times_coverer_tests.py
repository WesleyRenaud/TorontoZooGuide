from __future__ import annotations

from api.itinerary.scheduling.scheduled_activity_visit_times_coverer import ScheduledActivityVisitTimesCoverer


def Test_ArrivalCoveringStarts_TestUnsetArrival_ExpectNone() -> None:
   assert ScheduledActivityVisitTimesCoverer.arrival_covering_starts(
      None,
      [ '11:00', '10:00' ],
   ) is None


def Test_ArrivalCoveringStarts_TestEarlierExistingArrival_ExpectUnchanged() -> None:
   assert ScheduledActivityVisitTimesCoverer.arrival_covering_starts(
      '09:00',
      [ '10:00', '11:00' ],
   ) == '09:00'


def Test_ArrivalCoveringStarts_TestLaterExistingArrival_ExpectPulledEarlier() -> None:
   assert ScheduledActivityVisitTimesCoverer.arrival_covering_starts(
      '11:00',
      [ '10:00' ],
   ) == '10:00'


def Test_ArrivalCoveringStarts_TestNoStarts_ExpectExistingArrival() -> None:
   assert ScheduledActivityVisitTimesCoverer.arrival_covering_starts( '09:00', [] ) == '09:00'


def Test_DepartureCoveringEnds_TestUnsetDeparture_ExpectNone() -> None:
   assert ScheduledActivityVisitTimesCoverer.departure_covering_ends(
      None,
      [ '10:00', '11:30' ],
   ) is None


def Test_DepartureCoveringEnds_TestLaterExistingDeparture_ExpectUnchanged() -> None:
   assert ScheduledActivityVisitTimesCoverer.departure_covering_ends(
      '17:00',
      [ '10:00', '11:00' ],
   ) == '17:00'


def Test_DepartureCoveringEnds_TestEarlierExistingDeparture_ExpectPushedLater() -> None:
   assert ScheduledActivityVisitTimesCoverer.departure_covering_ends(
      '11:00',
      [ '11:30' ],
   ) == '11:30'


def Test_DepartureCoveringEnds_TestNoEnds_ExpectExistingDeparture() -> None:
   assert ScheduledActivityVisitTimesCoverer.departure_covering_ends( '17:00', [] ) == '17:00'
