from ... import zoo
from .wild_encounter_include_filter import WildEncounterIncludeFilter


def wild_encounter_record_to_model( record ):
   return zoo.WildEncounter(
      name=record.name,
      meeting_spot=record.meeting_spot,
      link=record.link,
      maximum_duration=record.maximum_duration,
      x_coord=record.x_coord,
      y_coord=record.y_coord )



def build_wild_encounter_details( wild_encounter_records, wild_encounters_to_include=None ):
   include_filter = WildEncounterIncludeFilter.from_optional_list(
      wild_encounters_to_include )

   if include_filter.should_return_empty():
      return []

   wild_encounters = []

   for record in wild_encounter_records:
      if not include_filter.allows_wild_encounter_name( record.name ):
         continue

      wild_encounters.append( wild_encounter_record_to_model( record ) )

   wild_encounters.sort( key=lambda w: ( w.name or '' ).lower() )

   return wild_encounters
