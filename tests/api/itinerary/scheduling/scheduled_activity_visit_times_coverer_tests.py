from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
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


def Test_EnsureArrivalCoversStart_TestEarlierStart_ExpectArrivalUpdated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   updated_times: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda connection, arrival_time: updated_times.append( arrival_time ) or True )

   assert ScheduledActivityVisitTimesCoverer.ensure_arrival_covers_start(
      conn,
      start_time='9:00 AM',
      current_arrival_time='9:30 AM' )
   assert updated_times == [ '9:00 AM' ]


def Test_EnsureArrivalCoversStart_TestLaterStart_ExpectUnchanged(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda connection, arrival_time: pytest.fail( 'arrival should not be updated' ) )

   assert not ScheduledActivityVisitTimesCoverer.ensure_arrival_covers_start(
      conn,
      start_time='10:00 AM',
      current_arrival_time='9:30 AM' )


def Test_EnsureDepartureCoversEnd_TestLaterEnd_ExpectDepartureUpdated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   updated_times: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda connection, departure_time: updated_times.append( departure_time ) or True )

   assert ScheduledActivityVisitTimesCoverer.ensure_departure_covers_end(
      conn,
      end_time='4:10 PM',
      current_departure_time='12:00 PM' )
   assert updated_times == [ '4:10 PM' ]


def Test_EnsureDepartureCoversEnd_TestEarlierEnd_ExpectUnchanged(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda connection, departure_time: pytest.fail( 'departure should not be updated' ) )

   assert not ScheduledActivityVisitTimesCoverer.ensure_departure_covers_end(
      conn,
      end_time='11:00 AM',
      current_departure_time='12:00 PM' )


def Test_CoverForActivity_TestScheduledActivity_ExpectEnsureAndSeed(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   calls: list[ str ] = []

   monkeypatch.setattr(
      ScheduledActivityVisitTimesCoverer,
      'ensure_arrival_covers_start',
      lambda *args, **kwargs: calls.append( 'arrival' ) or False )
   monkeypatch.setattr(
      ScheduledActivityVisitTimesCoverer,
      'ensure_departure_covers_end',
      lambda *args, **kwargs: calls.append( 'departure' ) or False )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ScheduledEndpointVisitTimesSyncer.seed_if_complete',
      lambda conn, itinerary: calls.append( 'seed' ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: type( 'SavedItinerary', (), {} )() )

   ScheduledActivityVisitTimesCoverer.cover_for_activity(
      conn,
      start_time='3:30 PM',
      end_time='4:15 PM',
      current_arrival_time='9:30 AM',
      current_departure_time='12:00 PM',
      itinerary_context={} )

   assert calls == [ 'arrival', 'departure', 'seed' ]
