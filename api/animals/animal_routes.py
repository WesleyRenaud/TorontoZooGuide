from __future__ import annotations

from .controllers.animal_controller import AnimalController
from ..json_request_handler import PostRouteHandler


class AnimalRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-visible-animals': AnimalController.get_visible_animals,
   '/get-animal-viewing-scopes': AnimalController.get_animal_viewing_scopes,
   '/get-animal-information': AnimalController.get_animal_information,
   '/get-animals-by-exhibit': AnimalController.get_animals_by_exhibit,
   '/get-animal-species-names': AnimalController.get_animal_species_names,
   '/get-exhibits-for-species': AnimalController.get_exhibits_for_species,
   '/get-off-display-animal-options': AnimalController.get_off_display_animal_options,
   '/get-off-display-exhibit-options': AnimalController.get_off_display_exhibit_options,
   '/get-off-display-viewing-scope-options': AnimalController.get_off_display_viewing_scope_options,
   '/get-animal-visibility-schedule-options': AnimalController.get_animal_visibility_schedule_options,
   '/get-animal-visibility-schedule-exhibit-options': AnimalController.get_animal_visibility_schedule_exhibit_options,
   '/get-animal-viewing-alert-options': AnimalController.get_animal_viewing_alert_options,
   '/get-animal-viewing-alert-exhibit-options': AnimalController.get_animal_viewing_alert_exhibit_options,
   '/set-animal-off-display': AnimalController.set_animal_off_display,
   '/set-animal-on-display': AnimalController.set_animal_on_display,
   '/set-animal-visibility-schedule': AnimalController.set_animal_visibility_schedule,
   '/remove-animal-visibility-schedule': AnimalController.remove_animal_visibility_schedule,
   '/set-animal-viewing-alert': AnimalController.set_animal_viewing_alert,
   '/remove-animal-viewing-alert': AnimalController.remove_animal_viewing_alert,
}

