from __future__ import annotations

from dataclasses import replace

from ...animals.controllers.animal_controller import AnimalController
from ...attractions.controllers.attraction_controller import AttractionController
from ..data_access.clear_itinerary import clear_itinerary
from ..data_access.itinerary import fetch_itinerary_date
from ..data_access.itinerary_save_input_mapper import map_itinerary_save_input
from ..data_access.save_itinerary import save_validated_itinerary
from ...guardians.controllers.guardians_controller import GuardiansController
from .itinerary_save_result import ItinerarySaveResult
from .itinerary_validation import validate_itinerary_for_save
from ...types import Connection, DateInput
from .wild_encounter_time_conflicts import remove_scheduled_items_with_time_conflicts
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController


def set_itinerary(
      conn: Connection,
      date: DateInput,
      animals: list[ dict[ str, str ] ],
      attractions: list[ str ],
      guardians_talks: list[ str ],
      wild_encounters: list[ str ],
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ] ) -> ItinerarySaveResult:
   save_input = map_itinerary_save_input(
      date,
      animals,
      attractions,
      guardians_talks,
      wild_encounters )
   old_visit_date = fetch_itinerary_date( conn )

   validated_itinerary = validate_itinerary_for_save(
      conn,
      save_input,
      animal_controller,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller,
      new_visit_date_temp=None,
      old_visit_date=old_visit_date )

   guardians_talks, wild_encounters, issues = remove_scheduled_items_with_time_conflicts(
      validated_itinerary.guardians_talks,
      validated_itinerary.wild_encounters )
   validated_itinerary = replace(
      validated_itinerary,
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters )

   clear_itinerary( conn )
   save_validated_itinerary( conn, save_input.date, validated_itinerary )

   return ItinerarySaveResult(
      success=True,
      issues=issues )
