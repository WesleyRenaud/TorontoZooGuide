from __future__ import annotations

import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.domain.itinerary_adjustment import ItineraryAdjustment
from api.itinerary.domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from api.itinerary.domain.itinerary_adjustment_type import ItineraryAdjustmentType
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


CURRENT_ITINERARY = ItineraryBuilder.build(
   date='2026-06-15',
   selected_exhibits=[],
   animals=[],
   attractions=[],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
   arrival_time='9:00 AM',
   departure_time='5:00 PM',
)

ITINERARY_CONTEXT = {
   'animal_coordinator': AnimalCoordinator,
   'attraction_coordinator': AttractionCoordinator,
   'guardians_coordinator': GuardiansCoordinator,
   'wild_encounter_coordinator': WildEncounterCoordinator,
   'visit_date_temp': None,
}

ADJUSTMENT = ItineraryAdjustment(
   type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
   field='arrivalTime',
   previous_value='9:00 AM',
   value='9:30 AM',
   reason=ItineraryAdjustmentReason.ARRIVAL_OUTSIDE_ADMISSION_HOURS,
)


@pytest.fixture
def save_result_builder_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def stub_saved_itinerary_build( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_save_result_builder.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: object() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_save_result_builder.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: CURRENT_ITINERARY )


def Test_SaveResult_TestErrorStatus_ExpectResultWithReasons(
      save_result_builder_conn: sqlite3.Connection,
      stub_saved_itinerary_build: None ) -> None:
   reason = ItineraryResultReason( code=ItineraryErrorType.TIME_OUT_OF_BOUNDS )

   result = ItinerarySaveResultBuilder.save_result(
      save_result_builder_conn,
      ItineraryErrorType.TIME_OUT_OF_BOUNDS,
      reasons=[ reason ],
      suppressed_warnings=[ ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE ],
      **ITINERARY_CONTEXT )

   assert result.status == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert result.reasons == [ reason ]
   assert result.suppressed_warnings == [ ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE ]
   assert result.itinerary == CURRENT_ITINERARY


def Test_SuccessResult_TestAdjustments_ExpectSuccessItinerary(
      save_result_builder_conn: sqlite3.Connection,
      stub_saved_itinerary_build: None ) -> None:
   result = ItinerarySaveResultBuilder.success_result(
      save_result_builder_conn,
      adjustments=[ ADJUSTMENT ],
      suppressed_warnings=[ ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP ],
      **ITINERARY_CONTEXT )

   assert result.status == ItineraryErrorType.SUCCESS
   assert result.adjustments == [ ADJUSTMENT ]
   assert result.suppressed_warnings == [ ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP ]
   assert result.itinerary == CURRENT_ITINERARY


def Test_PersistWalkRoute_TestContext_ExpectPersisterCalled(
      save_result_builder_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls: list[ dict[ str, object ] ] = []

   monkeypatch.setattr(
      'api.itinerary.routing.itinerary_walk_route_persister.ItineraryWalkRoutePersister.rebuild_and_persist',
      lambda conn, **context: calls.append( context ) )

   ItinerarySaveResultBuilder.persist_walk_route(
      save_result_builder_conn,
      **ITINERARY_CONTEXT )

   assert calls == [ ITINERARY_CONTEXT ]
