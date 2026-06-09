from __future__ import annotations

from .controllers.animal_controller import AnimalController
from ..json_handler import PostRouteHandler


ANIMAL_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-visible-animals': AnimalController.get_visible_animals,
   '/get-animal-viewing-scopes': AnimalController.get_animal_viewing_scopes,
   '/get-animal-information': AnimalController.get_animal_information,
   '/get-animals-by-exhibit': AnimalController.get_animals_by_exhibit,
   '/get-animal-species-names': AnimalController.get_animal_species_names,
   '/set-animal-off-display': AnimalController.set_animal_off_display,
   '/set-animal-on-display': AnimalController.set_animal_on_display,
   '/set-animal-visibility-schedule': AnimalController.set_animal_visibility_schedule,
   '/remove-animal-visibility-schedule': AnimalController.remove_animal_visibility_schedule,
   '/set-animal-viewing-alert': AnimalController.set_animal_viewing_alert,
   '/remove-animal-viewing-alert': AnimalController.remove_animal_viewing_alert,
}
