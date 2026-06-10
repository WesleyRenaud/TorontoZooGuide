from __future__ import annotations

from .controllers.update_controller import UpdateController
from ..json_handler import PostRouteHandler


UPDATE_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-updates': UpdateController.get_updates,
   '/get-active-update-options': UpdateController.get_active_update_options,
   '/create-update': UpdateController.create_update,
   '/end-update': UpdateController.end_update,
   '/edit-update': UpdateController.edit_update,
}
