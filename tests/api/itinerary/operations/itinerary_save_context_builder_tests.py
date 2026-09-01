from __future__ import annotations

import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.operations.itinerary_save_context_builder import ItinerarySaveContextBuilder
from api.models import Itinerary
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


@pytest.fixture
def context_builder_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_ControllerKwargs_TestCoordinators_ExpectKwargsDict() -> None:
   kwargs = ItinerarySaveContextBuilder.controller_kwargs(
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      visit_date_temp=72.0 )

   assert kwargs[ 'animal_coordinator' ] is AnimalCoordinator
   assert kwargs[ 'attraction_coordinator' ] is AttractionCoordinator
   assert kwargs[ 'guardians_coordinator' ] is GuardiansCoordinator
   assert kwargs[ 'wild_encounter_coordinator' ] is WildEncounterCoordinator
   assert kwargs[ 'visit_date_temp' ] == 72.0


def Test_CurrentItinerary_TestSavedItinerary_ExpectBuiltItinerary(
      context_builder_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_context_builder.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: object() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_context_builder.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: CURRENT_ITINERARY )

   controller_kwargs = ItinerarySaveContextBuilder.controller_kwargs(
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert ItinerarySaveContextBuilder.current_itinerary(
      context_builder_conn,
      controller_kwargs ) == CURRENT_ITINERARY


def Test_ErrorResult_TestStatus_ExpectSaveResultWithCurrentItinerary(
      context_builder_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItinerarySaveContextBuilder,
      'current_itinerary',
      lambda conn, itinerary_controller_kwargs: CURRENT_ITINERARY )

   result = ItinerarySaveContextBuilder.error_result(
      context_builder_conn,
      ItineraryErrorType.TIME_OUT_OF_BOUNDS,
      {
         'animal_coordinator': AnimalCoordinator,
         'attraction_coordinator': AttractionCoordinator,
         'guardians_coordinator': GuardiansCoordinator,
         'wild_encounter_coordinator': WildEncounterCoordinator,
      },
      suppressed_warnings=[ ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE ] )

   assert result.status == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert result.itinerary == CURRENT_ITINERARY
   assert result.suppressed_warnings == [ ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE ]
