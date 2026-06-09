from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace
from typing import Any

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.controllers.attraction_controller import AttractionController
from ..data_access.clear_itinerary import clear_itinerary
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.save_itinerary import save_validated_itinerary
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from .early_admission_warning import early_admission_warning_is_required
from ...guardians.controllers.guardians_controller import GuardiansController
from .guardians_talk_schedule_trimming import apply_guardians_talk_trimming
from .itinerary import build_current_itinerary
from .itinerary_adjustment import ItineraryAdjustment
from .itinerary_arrival_time_validation import arrival_time_is_valid_for_zoo_hours
from .itinerary_departure_time_validation import departure_time_is_valid_for_zoo_hours
from .itinerary_save_result import ItinerarySaveResult
from .itinerary_schedule_time_conflicts import schedule_time_conflict_warning
from .itinerary_suppressed_warnings import with_suppressed_warnings
from .itinerary_unschedule_confirmations import apply_confirmed_itinerary_unschedule_changes
from .itinerary_unschedule_confirmations import find_itinerary_unschedule_requirements
from .itinerary_unschedule_confirmations import ItineraryUnscheduleRequirements
from .itinerary_unschedule_confirmations import unschedule_confirmation_warning
from .itinerary_validation import validate_itinerary_for_save
from ...models import Itinerary
from ...shared.enums import ItineraryErrorType
from .short_visit_warning import short_visit_warning_is_required
from ...types import Connection
from .wild_encounter_time_conflicts import find_schedule_time_conflict_issues
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ...zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record


@dataclass( frozen=True )
class SetItineraryContext:
   conn: Connection
   save_input: ItinerarySaveInput
   validated_itinerary: ValidatedItinerary
   current_itinerary: Itinerary
   saved_itinerary: SavedItinerary | None
   unschedule_requirements: ItineraryUnscheduleRequirements
   itinerary_controller_kwargs: dict[ str, Any ]
   adjustments: tuple[ ItineraryAdjustment, ... ] = ()
   suppressed_warnings: tuple[ ItineraryErrorType, ... ] = ()


def itinerary_controller_kwargs(
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None = None ) -> dict[ str, Any ]:
   return {
      'animal_coordinator': animal_coordinator,
      'attraction_controller': attraction_controller,
      'guardians_controller': guardians_controller,
      'wild_encounter_controller': wild_encounter_controller,
      'visit_date_temp': visit_date_temp,
   }


def _build_current_itinerary_response(
      conn: Connection,
      itinerary_controller_kwargs: dict[ str, Any ] ) -> Itinerary:
   return build_current_itinerary(
      fetch_saved_itinerary( conn ),
      **itinerary_controller_kwargs )


def _build_error_result(
      conn: Connection,
      status: ItineraryErrorType,
      itinerary_controller_kwargs: dict[ str, Any ],
      *,
      suppressed_warnings: tuple[ ItineraryErrorType, ... ] = () ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      status=status,
      suppressed_warnings=suppressed_warnings,
      itinerary=_build_current_itinerary_response(
         conn,
         itinerary_controller_kwargs ) )


def validate_set_itinerary_zoo_hours(
      conn: Connection,
      save_input: ItinerarySaveInput,
      itinerary_controller_kwargs: dict[ str, Any ] ) -> ItinerarySaveResult | None:
   if (
         save_input.arrival_time is None
         or save_input.departure_time is None
   ):
      return None

   zoo_hours_record = fetch_zoo_hours_record(
      conn,
      save_input.date.isoformat() )

   arrival_time_error = arrival_time_is_valid_for_zoo_hours(
      save_input.arrival_time,
      zoo_hours_record,
      departure_time=save_input.departure_time )

   if arrival_time_error != ItineraryErrorType.SUCCESS:
      return _build_error_result(
         conn,
         arrival_time_error,
         itinerary_controller_kwargs )

   departure_time_error = departure_time_is_valid_for_zoo_hours(
      save_input.departure_time,
      zoo_hours_record,
      arrival_time=save_input.arrival_time )

   if departure_time_error != ItineraryErrorType.SUCCESS:
      return _build_error_result(
         conn,
         departure_time_error,
         itinerary_controller_kwargs )

   return None


def prepare_set_itinerary_context(
      conn: Connection,
      save_input: ItinerarySaveInput,
      *,
      old_visit_date: str | None,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None,
      itinerary_controller_kwargs: dict[ str, Any ],
      adjustments: tuple[ ItineraryAdjustment, ... ] = () ) -> SetItineraryContext:
   validated_itinerary = validate_itinerary_for_save(
      conn,
      save_input,
      animal_coordinator,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller,
      new_visit_date_temp=visit_date_temp,
      old_visit_date=old_visit_date )

   saved_itinerary = (
      fetch_saved_itinerary( conn )
      if old_visit_date is not None
      else None )

   response_saved_itinerary = (
      saved_itinerary
      if saved_itinerary is not None
      else fetch_saved_itinerary( conn ) )

   current_itinerary = build_current_itinerary(
      response_saved_itinerary,
      **itinerary_controller_kwargs )

   unschedule_requirements = (
      find_itinerary_unschedule_requirements(
         saved_itinerary,
         validated_itinerary )
      if saved_itinerary is not None
      else ItineraryUnscheduleRequirements( talks=(), encounters=() ) )

   return SetItineraryContext(
      conn=conn,
      save_input=save_input,
      validated_itinerary=validated_itinerary,
      current_itinerary=current_itinerary,
      saved_itinerary=saved_itinerary,
      unschedule_requirements=unschedule_requirements,
      itinerary_controller_kwargs=itinerary_controller_kwargs,
      adjustments=adjustments )


def check_set_itinerary_save_warnings(
      context: SetItineraryContext,
      *,
      confirming_short_visit: bool,
      confirming_early_admission: bool,
      confirming_guardians_talk_unschedule: bool,
      confirming_wild_encounter_unschedule: bool,
      overriding_conflicting_guardians_talks: bool ) -> tuple[
         SetItineraryContext,
         ItinerarySaveResult | None,
      ]:
   save_input = context.save_input
   controller_kwargs = context.itinerary_controller_kwargs
   suppressed_warnings: list[ ItineraryErrorType ] = []
   zoo_hours_record = (
      fetch_zoo_hours_record(
         context.conn,
         save_input.date.isoformat() )
      if save_input.arrival_time is not None
      else None )

   if (
         save_input.arrival_time is not None
         and early_admission_warning_is_required(
            context.conn,
            save_input.arrival_time,
            zoo_hours_record,
            confirming_early_admission=confirming_early_admission,
            suppressed_warnings=suppressed_warnings )
   ):
      warning_tuple = tuple( suppressed_warnings )
      return (
         replace( context, suppressed_warnings=warning_tuple ),
         _build_error_result(
            context.conn,
            ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
            controller_kwargs,
            suppressed_warnings=warning_tuple ),
      )

   if (
         save_input.arrival_time is not None
         and save_input.departure_time is not None
         and short_visit_warning_is_required(
            context.conn,
            save_input.arrival_time,
            save_input.departure_time,
            confirming_short_visit=confirming_short_visit,
            suppressed_warnings=suppressed_warnings )
   ):
      warning_tuple = tuple( suppressed_warnings )
      return (
         replace( context, suppressed_warnings=warning_tuple ),
         _build_error_result(
            context.conn,
            ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
            controller_kwargs,
            suppressed_warnings=warning_tuple ),
      )

   warning_tuple = tuple( suppressed_warnings )
   updated_context = replace( context, suppressed_warnings=warning_tuple )

   schedule_conflict_warning = schedule_time_conflict_warning(
      context.validated_itinerary.guardians_talks,
      context.validated_itinerary.wild_encounters,
      context.current_itinerary,
      overriding_conflicting_guardians_talks=(
         overriding_conflicting_guardians_talks ) )

   if schedule_conflict_warning is not None:
      return (
         updated_context,
         with_suppressed_warnings( schedule_conflict_warning, warning_tuple ),
      )

   if context.saved_itinerary is not None:
      unschedule_warning = unschedule_confirmation_warning(
         context.unschedule_requirements,
         context.current_itinerary,
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ),
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ) )

      if unschedule_warning is not None:
         return (
            updated_context,
            with_suppressed_warnings( unschedule_warning, warning_tuple ),
         )

   return ( updated_context, None )


def commit_set_itinerary(
      context: SetItineraryContext,
      *,
      overriding_conflicting_guardians_talks: bool ) -> ItinerarySaveResult:
   validated_itinerary = context.validated_itinerary

   if overriding_conflicting_guardians_talks:
      trimmed_guardians_talks = apply_guardians_talk_trimming(
         validated_itinerary.guardians_talks,
         validated_itinerary.wild_encounters )
      validated_itinerary = replace(
         validated_itinerary,
         guardians_talks=trimmed_guardians_talks )

   if context.saved_itinerary is not None:
      validated_itinerary = apply_confirmed_itinerary_unschedule_changes(
         validated_itinerary,
         context.unschedule_requirements )

   remaining_conflicts = find_schedule_time_conflict_issues(
      validated_itinerary.guardians_talks,
      validated_itinerary.wild_encounters )

   if remaining_conflicts:
      return ItinerarySaveResult(
         status=ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT,
         reasons=remaining_conflicts,
         suppressed_warnings=context.suppressed_warnings,
         itinerary=context.current_itinerary )

   clear_itinerary( context.conn )
   save_validated_itinerary(
      context.conn,
      context.save_input.date,
      validated_itinerary )

   return ItinerarySaveResult(
      adjustments=context.adjustments,
      suppressed_warnings=context.suppressed_warnings,
      itinerary=_build_current_itinerary_response(
         context.conn,
         context.itinerary_controller_kwargs ) )
