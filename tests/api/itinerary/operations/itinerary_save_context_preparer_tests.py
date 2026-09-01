from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.conflicts.itinerary_unschedule_requirements import ItineraryUnscheduleRequirements
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.domain.itinerary_adjustment import ItineraryAdjustment
from api.itinerary.domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from api.itinerary.domain.itinerary_adjustment_type import ItineraryAdjustmentType
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.operations.itinerary_save_context_preparer import ItinerarySaveContextPreparer
from api.models.animal_diff import AnimalDiff
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


SAVE_INPUT = ItinerarySaveInput(
   date=date( 2026, 6, 22 ),
   arrival_time='09:30',
   departure_time='17:00',
   animals=[ ItineraryAnimalInput( species='African Lion', exhibit='Africa Savanna' ) ],
)

VALIDATED_ITINERARY = ValidatedItinerary(
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animals=[
      AnimalDiff(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100 ),
   ],
   attractions=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
)

SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
)

UNSCHEDULE_REQUIREMENTS = ItineraryUnscheduleRequirements(
   talks=[],
   encounters=[],
)

ADJUSTMENTS = [
   ItineraryAdjustment(
      type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
      field='arrivalTime',
      previous_value='9:00 AM',
      value='9:30 AM',
      reason=ItineraryAdjustmentReason.ARRIVAL_OUTSIDE_ADMISSION_HOURS ),
]

CONTROLLER_KWARGS = {
   'animal_coordinator': AnimalCoordinator,
   'attraction_coordinator': AttractionCoordinator,
   'guardians_coordinator': GuardiansCoordinator,
   'wild_encounter_coordinator': WildEncounterCoordinator,
   'visit_date_temp': None,
}


@pytest.fixture
def preparer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_Prepare_TestOwnedSaveInput_ExpectSaveContextWithValidatedItinerary(
      preparer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_context_preparer.ItinerarySaveValidator.validate_for_save',
      lambda conn, save_input, *coordinators, **kwargs: VALIDATED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_context_preparer.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_context_preparer.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_context_preparer.ItineraryUnscheduleRequirementsFinder.find',
      lambda saved_itinerary, validated_itinerary: UNSCHEDULE_REQUIREMENTS )

   context = ItinerarySaveContextPreparer.prepare(
      preparer_conn,
      SAVE_INPUT,
      old_visit_date='2026-06-20',
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      visit_date_temp=None,
      itinerary_controller_kwargs=CONTROLLER_KWARGS,
      adjustments=ADJUSTMENTS )

   assert context.conn is preparer_conn
   assert context.save_input == SAVE_INPUT
   assert context.validated_itinerary == VALIDATED_ITINERARY
   assert context.saved_itinerary == SAVED_ITINERARY
   assert context.old_visit_date == '2026-06-20'
   assert context.unschedule_requirements == UNSCHEDULE_REQUIREMENTS
   assert context.adjustments == ADJUSTMENTS


def Test_Prepare_TestWithoutOldVisitDate_ExpectNoSavedItinerary(
      preparer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_context_preparer.ItinerarySaveValidator.validate_for_save',
      lambda conn, save_input, *coordinators, **kwargs: VALIDATED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_context_preparer.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_context_preparer.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: ItineraryBuilder.empty() )

   context = ItinerarySaveContextPreparer.prepare(
      preparer_conn,
      SAVE_INPUT,
      old_visit_date=None,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      visit_date_temp=None,
      itinerary_controller_kwargs=CONTROLLER_KWARGS )

   assert context.saved_itinerary is None
   assert context.unschedule_requirements.talks == []
   assert context.unschedule_requirements.encounters == []
