def species_exhibit_key_from_values( species, exhibit ):
   return (
      ( species or '' ).strip().lower(),
      ( exhibit or '' ).strip().lower(),
   )


def species_exhibit_key( animal ):
   return species_exhibit_key_from_values( animal.species, animal.exhibit )


def animal_matches_query( animal, query_lower ):
   species, exhibit = species_exhibit_key( animal )
   return query_lower in species or query_lower in exhibit


def filter_animals_matching_query( animals, query ):
   if not query:
      return list( animals )

   query_lower = query.strip().lower()
   return [
      animal for animal in animals
      if animal_matches_query( animal, query_lower )
   ]


def filter_animals_by_species_exhibit_keys( animals, species_exhibit_keys ):
   keys = set( species_exhibit_keys )

   if not keys:
      return []

   return [
      animal for animal in animals
      if species_exhibit_key( animal ) in keys
   ]


def dedupe_animals_by_species_and_exhibit( animals ):
   best_by_species_and_exhibit = {}

   for animal in animals:
      key = species_exhibit_key( animal )
      current = best_by_species_and_exhibit.get( key )
      if current is None or ( animal.likelihood or 0 ) > ( current.likelihood or 0 ):
         best_by_species_and_exhibit[ key ] = animal

   return list( best_by_species_and_exhibit.values() )


def sort_animals_by_species_and_exhibit( animals ):
   sorted_animals = list( animals )
   sorted_animals.sort( key=species_exhibit_key )
   return sorted_animals


def build_animals_matching_query( animals, query ):
   animals = filter_animals_matching_query( animals, query )
   animals = dedupe_animals_by_species_and_exhibit( animals )
   return sort_animals_by_species_and_exhibit( animals )
