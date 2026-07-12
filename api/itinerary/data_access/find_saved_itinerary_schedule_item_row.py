from __future__ import annotations

from ..animal_item_key import AnimalScheduleItemKey
from ...animals.search.animals_matching_query import viewing_spot_key_from_values
from ..attraction_item_key import AttractionScheduleItemKey
from ..guardians_talk_item_key import GuardiansTalkScheduleItemKey
from .itinerary_animal_record import ItineraryAnimalRecord
from .itinerary_attraction_record import ItineraryAttractionRecord
from .itinerary_event_record import ItineraryEventRecord
from .itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from .itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from .saved_itinerary import SavedItinerary
from ..scheduling.items.schedule_item_key import ScheduleItemKey
from ...shared.enums import ItineraryEventType
from ..wild_encounter_item_key import WildEncounterScheduleItemKey


SavedItineraryScheduleItemRow = (
   ItineraryAnimalRecord
   | ItineraryAttractionRecord
   | ItineraryGuardiansTalkRecord
   | ItineraryWildEncounterRecord
   | ItineraryEventRecord
)


def _animal_row_matches_schedule_item_key(
      animal_row: ItineraryAnimalRecord,
      schedule_item_key: AnimalScheduleItemKey ) -> bool:
   return animal_row.viewing_spot_key() == viewing_spot_key_from_values(
      schedule_item_key.species,
      schedule_item_key.exhibit,
      schedule_item_key.enclosure_name )


def _attraction_row_matches_schedule_item_key(
      attraction_row: ItineraryAttractionRecord,
      schedule_item_key: AttractionScheduleItemKey ) -> bool:
   return attraction_row.attraction == schedule_item_key.name


def _guardians_talk_row_matches_schedule_item_key(
      talk_row: ItineraryGuardiansTalkRecord,
      schedule_item_key: GuardiansTalkScheduleItemKey ) -> bool:
   if talk_row.is_deleted:
      return False

   row_key = GuardiansTalkScheduleItemKey.from_row( talk_row )

   return row_key == schedule_item_key


def _wild_encounter_row_matches_schedule_item_key(
      encounter_row: ItineraryWildEncounterRecord,
      schedule_item_key: WildEncounterScheduleItemKey ) -> bool:
   if encounter_row.is_deleted:
      return False

   row_key = WildEncounterScheduleItemKey.from_row( encounter_row )

   return row_key == schedule_item_key


def _event_row_matches_schedule_item_key(
      event_row: ItineraryEventRecord,
      event_type: ItineraryEventType ) -> bool:
   return event_row.event_type == event_type


def find_saved_itinerary_schedule_item_row(
      saved_itinerary: SavedItinerary,
      schedule_item_key: ScheduleItemKey,
      ) -> SavedItineraryScheduleItemRow | None:
   if isinstance( schedule_item_key, AnimalScheduleItemKey ):
      return next(
         (
            animal_row
            for animal_row in saved_itinerary.animal_rows
            if _animal_row_matches_schedule_item_key(
               animal_row,
               schedule_item_key )
         ),
         None,
      )

   if isinstance( schedule_item_key, AttractionScheduleItemKey ):
      return next(
         (
            attraction_row
            for attraction_row in saved_itinerary.attraction_rows
            if _attraction_row_matches_schedule_item_key(
               attraction_row,
               schedule_item_key )
         ),
         None,
      )

   if isinstance( schedule_item_key, GuardiansTalkScheduleItemKey ):
      return next(
         (
            talk_row
            for talk_row in saved_itinerary.guardians_talk_rows
            if _guardians_talk_row_matches_schedule_item_key(
               talk_row,
               schedule_item_key )
         ),
         None,
      )

   if isinstance( schedule_item_key, WildEncounterScheduleItemKey ):
      return next(
         (
            encounter_row
            for encounter_row in saved_itinerary.wild_encounter_rows
            if _wild_encounter_row_matches_schedule_item_key(
               encounter_row,
               schedule_item_key )
         ),
         None,
      )

   if isinstance( schedule_item_key, ItineraryEventType ):
      return next(
         (
            event_row
            for event_row in saved_itinerary.event_rows
            if _event_row_matches_schedule_item_key(
               event_row,
               schedule_item_key )
         ),
         None,
      )

   return None
