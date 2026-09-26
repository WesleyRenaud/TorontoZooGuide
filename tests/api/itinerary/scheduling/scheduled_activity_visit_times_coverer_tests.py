from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.scheduled_activity_visit_times_coverer import ScheduledActivityVisitTimesCoverer


def Test_ArrivalCoveringStarts_TestUnsetArrival_ExpectNone() -> None:
   starts = [ '11:00', '10:00' ]

   arrival = ScheduledActivityVisitTimesCoverer.arrival_covering_starts(
      None,
      starts )

   assert arrival is None


def Test_ArrivalCoveringStarts_TestEarlierExistingArrival_ExpectUnchanged() -> None:
   existing_arrival = '09:00'
   starts = [ '10:00', '11:00' ]

   arrival = ScheduledActivityVisitTimesCoverer.arrival_covering_starts(
      existing_arrival,
      starts )

   assert arrival == existing_arrival


def Test_ArrivalCoveringStarts_TestLaterExistingArrival_ExpectPulledEarlier() -> None:
   existing_arrival = '11:00'
   earlier_start = '10:00'

   arrival = ScheduledActivityVisitTimesCoverer.arrival_covering_starts(
      existing_arrival,
      [ earlier_start ] )

   assert arrival == earlier_start


def Test_ArrivalCoveringStarts_TestNoStarts_ExpectExistingArrival() -> None:
   existing_arrival = '09:00'

   arrival = ScheduledActivityVisitTimesCoverer.arrival_covering_starts(
      existing_arrival,
      [] )

   assert arrival == existing_arrival


def Test_DepartureCoveringEnds_TestUnsetDeparture_ExpectNone() -> None:
   ends = [ '10:00', '11:30' ]

   departure = ScheduledActivityVisitTimesCoverer.departure_covering_ends(
      None,
      ends )

   assert departure is None


def Test_DepartureCoveringEnds_TestLaterExistingDeparture_ExpectUnchanged() -> None:
   existing_departure = '17:00'
   ends = [ '10:00', '11:00' ]

   departure = ScheduledActivityVisitTimesCoverer.departure_covering_ends(
      existing_departure,
      ends )

   assert departure == existing_departure


def Test_DepartureCoveringEnds_TestEarlierExistingDeparture_ExpectPushedLater() -> None:
   existing_departure = '11:00'
   later_end = '11:30'

   departure = ScheduledActivityVisitTimesCoverer.departure_covering_ends(
      existing_departure,
      [ later_end ] )

   assert departure == later_end


def Test_DepartureCoveringEnds_TestNoEnds_ExpectExistingDeparture() -> None:
   existing_departure = '17:00'

   departure = ScheduledActivityVisitTimesCoverer.departure_covering_ends(
      existing_departure,
      [] )

   assert departure == existing_departure


def Test_EnsureArrivalCoversStart_TestEarlierStart_ExpectArrivalUpdated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   start_time = '9:00 AM'
   current_arrival_time = '9:30 AM'
   updated_times: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda connection, arrival_time: updated_times.append( arrival_time ) or True )

   updated = ScheduledActivityVisitTimesCoverer.ensure_arrival_covers_start(
      conn,
      start_time=start_time,
      current_arrival_time=current_arrival_time )

   assert updated
   assert updated_times == [ start_time ]


def Test_EnsureArrivalCoversStart_TestLaterStart_ExpectUnchanged(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   start_time = '10:00 AM'
   current_arrival_time = '9:30 AM'

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryTimeProvider.set_itinerary_arrival_time',
      lambda connection, arrival_time: pytest.fail( 'arrival should not be updated' ) )

   updated = ScheduledActivityVisitTimesCoverer.ensure_arrival_covers_start(
      conn,
      start_time=start_time,
      current_arrival_time=current_arrival_time )

   assert not updated


def Test_EnsureDepartureCoversEnd_TestLaterEnd_ExpectDepartureUpdated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   end_time = '4:10 PM'
   current_departure_time = '12:00 PM'
   updated_times: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda connection, departure_time: updated_times.append( departure_time ) or True )

   updated = ScheduledActivityVisitTimesCoverer.ensure_departure_covers_end(
      conn,
      end_time=end_time,
      current_departure_time=current_departure_time )

   assert updated
   assert updated_times == [ end_time ]


def Test_EnsureDepartureCoversEnd_TestEarlierEnd_ExpectUnchanged(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   end_time = '11:00 AM'
   current_departure_time = '12:00 PM'

   monkeypatch.setattr(
      'api.itinerary.scheduling.scheduled_activity_visit_times_coverer.ItineraryTimeProvider.set_itinerary_departure_time',
      lambda connection, departure_time: pytest.fail( 'departure should not be updated' ) )

   updated = ScheduledActivityVisitTimesCoverer.ensure_departure_covers_end(
      conn,
      end_time=end_time,
      current_departure_time=current_departure_time )

   assert not updated


def Test_CoverForActivity_TestScheduledActivity_ExpectEnsureAndSeed(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   start_time = '3:30 PM'
   end_time = '4:15 PM'
   current_arrival_time = '9:30 AM'
   current_departure_time = '12:00 PM'
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
      start_time=start_time,
      end_time=end_time,
      current_arrival_time=current_arrival_time,
      current_departure_time=current_departure_time,
      itinerary_context={} )

   assert calls == [ 'arrival', 'departure', 'seed' ]


def Test_CoverForActivity_TestSeedDisabled_ExpectEnsureOnly(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   start_time = '3:30 PM'
   end_time = '4:15 PM'
   current_arrival_time = '9:30 AM'
   current_departure_time = '12:00 PM'
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

   ScheduledActivityVisitTimesCoverer.cover_for_activity(
      conn,
      start_time=start_time,
      end_time=end_time,
      current_arrival_time=current_arrival_time,
      current_departure_time=current_departure_time,
      itinerary_context={},
      seed_if_complete=False )

   assert calls == [ 'arrival', 'departure' ]
