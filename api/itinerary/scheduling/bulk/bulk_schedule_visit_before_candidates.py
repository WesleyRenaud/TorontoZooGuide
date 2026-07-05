from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ....walk_graph.viewing_spot_routing_overrides import bulk_schedule_visit_before_rules


def bulk_schedule_candidate_animals_after_visit_before_rules(
      candidate_animals: list[ ItineraryAnimalRecord ],
      *,
      fallback_animals: list[ ItineraryAnimalRecord ] | None = None ) -> list[
         ItineraryAnimalRecord ]:
   remaining_animals = fallback_animals or candidate_animals
   remaining_keys = {
      animal_row.viewing_spot_key()
      for animal_row in remaining_animals
   }
   blocked_keys: set[ tuple[ str, str, str | None ] ] = set()

   for rule in bulk_schedule_visit_before_rules():
      visit_first_key = rule.visit_first.key()

      if visit_first_key not in remaining_keys:
         continue

      blocked_before_keys = {
         viewing_spot.key()
         for viewing_spot in rule.visit_before
         if viewing_spot.key() in remaining_keys
      }

      if not blocked_before_keys:
         continue

      blocked_keys.update( blocked_before_keys )

   if not blocked_keys:
      return candidate_animals

   filtered_animals = [
      animal_row
      for animal_row in candidate_animals
      if animal_row.viewing_spot_key() not in blocked_keys
   ]

   if filtered_animals:
      return filtered_animals

   return candidate_animals
