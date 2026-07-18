from __future__ import annotations

from typing import Any

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..conflicts.itinerary_unschedule_confirmations import find_itinerary_unschedule_requirements
from ..conflicts.itinerary_unschedule_confirmations import ItineraryUnscheduleRequirements
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..domain.itinerary import build_current_itinerary
from ..domain.itinerary_adjustment import ItineraryAdjustment
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .set_itinerary_context import SetItineraryContext
from ...types import Connection
from ..validation.itinerary_validation import validate_itinerary_for_save
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def prepare_set_itinerary_context(
      conn: Connection,
      save_input: ItinerarySaveInput,
      *,
      old_visit_date: str | None,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None,
      itinerary_controller_kwargs: dict[ str, Any ],
      adjustments: list[ ItineraryAdjustment ] | None = None ) -> SetItineraryContext:
   validated_itinerary = validate_itinerary_for_save(
      conn,
      save_input,
      animal_coordinator,
      attraction_coordinator,
      guardians_coordinator,
      wild_encounter_coordinator,
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
      else ItineraryUnscheduleRequirements( talks=[], encounters=[] ) )

   return SetItineraryContext(
      conn=conn,
      save_input=save_input,
      validated_itinerary=validated_itinerary,
      current_itinerary=current_itinerary,
      old_visit_date=old_visit_date,
      saved_itinerary=saved_itinerary,
      unschedule_requirements=unschedule_requirements,
      itinerary_controller_kwargs=itinerary_controller_kwargs,
      adjustments=adjustments or [] )
