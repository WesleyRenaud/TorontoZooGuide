from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.conflicts.itinerary_unschedule_requirements import ItineraryUnscheduleRequirements
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.operations.itinerary_save_context import ItinerarySaveContext
from api.itinerary.operations.itinerary_save_warning_checker import ItinerarySaveWarningChecker
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


SAVE_INPUT = ItinerarySaveInput(
   date=date( 2026, 6, 15 ),
   arrival_time='08:30',
   departure_time='17:00',
)

VALIDATED_ITINERARY = ValidatedItinerary(
   arrival_time='8:30 AM',
   departure_time='5:00 PM',
   animals=[],
   attractions=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
)

CONTROLLER_KWARGS = {
   'animal_coordinator': AnimalCoordinator,
   'attraction_coordinator': AttractionCoordinator,
   'guardians_coordinator': GuardiansCoordinator,
   'wild_encounter_coordinator': WildEncounterCoordinator,
   'visit_date_temp': None,
}


def _save_context(
      conn: sqlite3.Connection,
      *,
      saved_itinerary: SavedItinerary | None = None ) -> ItinerarySaveContext:
   return ItinerarySaveContext(
      conn=conn,
      save_input=SAVE_INPUT,
      validated_itinerary=VALIDATED_ITINERARY,
      current_itinerary=ItineraryBuilder.empty(),
      old_visit_date='2026-06-14',
      saved_itinerary=saved_itinerary,
      unschedule_requirements=ItineraryUnscheduleRequirements( talks=[], encounters=[] ),
      itinerary_controller_kwargs=CONTROLLER_KWARGS )


@pytest.fixture
def warning_checker_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_Check_TestEarlyAdmissionRequired_ExpectWarningResult(
      warning_checker_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, date_value: object() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.EarlyAdmissionWarningBuilder.is_required',
      lambda conn, arrival_time, zoo_hours_record, **kwargs: True )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ItinerarySaveContextBuilder.error_result',
      lambda conn, status, controller_kwargs, **kwargs: ItinerarySaveResult(
         status=status,
         suppressed_warnings=kwargs.get( 'suppressed_warnings', [] ),
         itinerary=ItineraryBuilder.empty() ) )

   updated_context, warning = ItinerarySaveWarningChecker.check(
      _save_context( warning_checker_conn ),
      confirming_short_visit=False,
      confirming_early_admission=False,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=False,
      confirming_guardians_talk_without_animal=False,
      confirming_attraction_without_animal=False,
      overriding_conflicting_guardians_talks=False )

   assert warning is not None
   assert warning.status == ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
   assert updated_context.suppressed_warnings == []


def Test_Check_TestShortVisitRequired_ExpectWarningResult(
      warning_checker_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, date_value: object() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.EarlyAdmissionWarningBuilder.is_required',
      lambda conn, arrival_time, zoo_hours_record, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ShortVisitWarningBuilder.is_required',
      lambda conn, arrival_time, departure_time, **kwargs: True )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ItinerarySaveContextBuilder.error_result',
      lambda conn, status, controller_kwargs, **kwargs: ItinerarySaveResult(
         status=status,
         suppressed_warnings=kwargs.get( 'suppressed_warnings', [] ),
         itinerary=ItineraryBuilder.empty() ) )

   updated_context, warning = ItinerarySaveWarningChecker.check(
      _save_context( warning_checker_conn ),
      confirming_short_visit=False,
      confirming_early_admission=True,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=False,
      confirming_guardians_talk_without_animal=False,
      confirming_attraction_without_animal=False,
      overriding_conflicting_guardians_talks=False )

   assert warning is not None
   assert warning.status == ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
   assert updated_context.suppressed_warnings == []


def Test_Check_TestUnscheduleConfirmation_ExpectPendingReason(
      warning_checker_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:30 PM',
      location='Africa Savanna' )
   unschedule_warning = ItinerarySaveResult(
      status=ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      reasons=[
         ItineraryResultReason(
            code=ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS ),
      ],
      itinerary=ItineraryBuilder.empty() )

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, date_value: object() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.EarlyAdmissionWarningBuilder.is_required',
      lambda conn, arrival_time, zoo_hours_record, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ShortVisitWarningBuilder.is_required',
      lambda conn, arrival_time, departure_time, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ItineraryScheduleTimeConflictWarningBuilder.build',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ItineraryUnscheduleConfirmationWarningBuilder.build',
      lambda *args, **kwargs: unschedule_warning )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.GuardiansTalkWithoutAnimalWarningBuilder.is_required',
      lambda *args, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.AttractionWithoutAnimalWarningBuilder.is_required',
      lambda *args, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items',
      lambda validated_itinerary: False )

   context = _save_context(
      warning_checker_conn,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-14',
         arrival_time='9:00 AM',
         departure_time='5:00 PM',
      ) )
   context = ItinerarySaveContext(
      conn=context.conn,
      save_input=context.save_input,
      validated_itinerary=ValidatedItinerary(
         arrival_time='9:00 AM',
         departure_time='5:00 PM',
         animals=[],
         attractions=[],
         guardians_talks=[ talk ],
         wild_encounters=[],
         events=[],
      ),
      current_itinerary=context.current_itinerary,
      old_visit_date=context.old_visit_date,
      saved_itinerary=context.saved_itinerary,
      unschedule_requirements=ItineraryUnscheduleRequirements( talks=[ talk ], encounters=[] ),
      itinerary_controller_kwargs=context.itinerary_controller_kwargs )

   updated_context, warning = ItinerarySaveWarningChecker.check(
      context,
      confirming_short_visit=True,
      confirming_early_admission=True,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=False,
      confirming_guardians_talk_without_animal=False,
      confirming_attraction_without_animal=False,
      overriding_conflicting_guardians_talks=False )

   assert warning is not None
   assert warning.status == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert len( warning.reasons ) == 1


def Test_Check_TestNoWarnings_ExpectNone(
      warning_checker_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, date_value: object() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.EarlyAdmissionWarningBuilder.is_required',
      lambda conn, arrival_time, zoo_hours_record, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ShortVisitWarningBuilder.is_required',
      lambda conn, arrival_time, departure_time, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.ItineraryScheduleTimeConflictWarningBuilder.build',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.GuardiansTalkWithoutAnimalWarningBuilder.is_required',
      lambda *args, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.AttractionWithoutAnimalWarningBuilder.is_required',
      lambda *args, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_warning_checker.FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items',
      lambda validated_itinerary: False )

   updated_context, warning = ItinerarySaveWarningChecker.check(
      _save_context( warning_checker_conn ),
      confirming_short_visit=True,
      confirming_early_admission=True,
      confirming_guardians_talk_unschedule=True,
      confirming_wild_encounter_unschedule=True,
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True,
      confirming_attraction_without_animal=True,
      overriding_conflicting_guardians_talks=False )

   assert warning is None
   assert updated_context.suppressed_warnings == []
