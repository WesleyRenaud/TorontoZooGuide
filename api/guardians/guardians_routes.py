from __future__ import annotations

from .controllers.guardians_controller import GuardiansController
from ..json_request_handler import PostRouteHandler


class GuardiansRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-guardians-talks': GuardiansController.get_guardians_talks,
   '/get-guardians-talk-locations': GuardiansController.get_guardians_talk_locations,
   '/get-guardians-talk-names': GuardiansController.get_guardians_talk_names,
   '/get-guardians-talk-names-at-location': (
      GuardiansController.get_guardians_talk_names_at_location
   ),
   '/get-guardians-talk-occurrences': GuardiansController.get_guardians_talk_occurrences,
   '/get-guardians-talk-schedule-times': GuardiansController.get_guardians_talk_schedule_times,
   '/set-guardians-talk-schedule': GuardiansController.set_guardians_talk_schedule,
   '/replace-guardians-talk-schedule-overlaps': (
      GuardiansController.replace_guardians_talk_schedule_overlaps
   ),
   '/trim-guardians-talk-schedule-overlaps': (
      GuardiansController.trim_guardians_talk_schedule_overlaps
   ),
   '/end-guardians-talk-schedule': GuardiansController.end_guardians_talk_schedule,
   '/add-guardians-talk-occurrence': GuardiansController.add_guardians_talk_occurrence,
   '/cancel-guardians-talk-occurrence': GuardiansController.cancel_guardians_talk_occurrence,
}

