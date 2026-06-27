from __future__ import annotations

from .controllers.wild_encounter_controller import WildEncounterController
from ..json_handler import PostRouteHandler


WILD_ENCOUNTER_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-wild-encounters': WildEncounterController.get_wild_encounters,
   '/get-wild-encounter-names': WildEncounterController.get_wild_encounter_names,
   '/get-wild-encounter-occurrences': WildEncounterController.get_wild_encounter_occurrences,
   '/get-wild-encounter-schedule-times': WildEncounterController.get_wild_encounter_schedule_times,
   '/set-wild-encounter-schedule': WildEncounterController.set_wild_encounter_schedule,
   '/end-wild-encounter-schedule': WildEncounterController.end_wild_encounter_schedule,
   '/cancel-wild-encounter-occurrence': WildEncounterController.cancel_wild_encounter_occurrence,
}
