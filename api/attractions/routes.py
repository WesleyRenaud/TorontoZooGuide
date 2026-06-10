from __future__ import annotations

from .controllers.attraction_controller import AttractionController
from ..json_handler import PostRouteHandler


ATTRACTION_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-attractions': AttractionController.get_attractions,
   '/get-attraction-names': AttractionController.get_attraction_names,
   '/set-attraction-closed': AttractionController.set_attraction_closed,
   '/set-attraction-closure-override': AttractionController.set_attraction_closure_override,
   '/set-attraction-opening-schedule': AttractionController.set_attraction_opening_schedule,
   '/replace-attraction-opening-schedule-overlaps': (
      AttractionController.replace_attraction_opening_schedule_overlaps
   ),
   '/trim-attraction-opening-schedule-overlaps': (
      AttractionController.trim_attraction_opening_schedule_overlaps
   ),
}
