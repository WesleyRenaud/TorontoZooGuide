from __future__ import annotations


def normalize_update_type( update_type: str ) -> str | None:
   update_type_labels = {
      'animal birth': 'Animal Birth',
      'animal_birth': 'Animal Birth',
      'animal passing': 'Animal Passing',
      'animal_passing': 'Animal Passing',
      'closure': 'Closure',
      'new arrival': 'New Arrival',
      'new_arrival': 'New Arrival',
      'departure': 'Departure'
   }

   normalized_key = str( update_type ).strip().lower()

   return update_type_labels.get( normalized_key )
