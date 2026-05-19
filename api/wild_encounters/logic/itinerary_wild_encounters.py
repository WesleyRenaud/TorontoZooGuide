from ...itinerary.data_access.itinerary_name_key import itinerary_name_key


def build_itinerary_wild_encounters( wild_encounters, saved_wild_encounters ):
   wild_encounter_by_name = {
      saved_encounter.name_key(): saved_encounter
      for saved_encounter in saved_wild_encounters
   }

   for wild_encounter in wild_encounters:
      saved_encounter = wild_encounter_by_name.get(
         itinerary_name_key( wild_encounter.name ) )

      if saved_encounter == None:
         continue

      wild_encounter.start_time = saved_encounter.start_time
      wild_encounter.end_time = saved_encounter.end_time
      wild_encounter.is_deleted = saved_encounter.is_deleted

   wild_encounters.sort(
      key=lambda wild_encounter: (
         ( wild_encounter.name or '' ).lower(),
         wild_encounter.start_time or ''
      )
   )

   return wild_encounters
