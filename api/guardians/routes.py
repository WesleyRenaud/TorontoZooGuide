from __future__ import annotations

from .controllers.guardians_controller import GuardiansController
from ..json_handler import PostRouteHandler


GUARDIANS_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-guardians-talks': GuardiansController.get_guardians_talks,
   '/get-guardians-talk-locations': GuardiansController.get_guardians_talk_locations,
   '/get-guardians-talk-names': GuardiansController.get_guardians_talk_names,
   '/get-guardians-talk-names-at-location': (
      GuardiansController.get_guardians_talk_names_at_location
   ),
   '/get-guardians-talk-occurrences': GuardiansController.get_guardians_talk_occurrences,
   '/set-guardians-talk-schedule': GuardiansController.set_guardians_talk_schedule,
   '/end-guardians-talk-schedule': GuardiansController.end_guardians_talk_schedule,
   '/cancel-guardians-talk-occurrence': GuardiansController.cancel_guardians_talk_occurrence,
}
