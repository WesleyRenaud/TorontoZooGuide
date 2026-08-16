from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from .itinerary_animal_record import ItineraryAnimalRecord
from .itinerary_attraction_record import ItineraryAttractionRecord
from .itinerary_event_record import ItineraryEventRecord
from .itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from .itinerary_transportation_record import ItineraryTransportationRecord
from .itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ...shared.calendar_dates import DateValues
from ...types import DateInput, ScheduleTimeKey


@dataclass( frozen=True )
class SavedItinerary:
   date_value: DateInput | None
   arrival_time: ScheduleTimeKey
   departure_time: ScheduleTimeKey
   selected_exhibits: list[ str ] = field( default_factory=list )
   animal_rows: list[ ItineraryAnimalRecord ] = field( default_factory=list )
   attraction_rows: list[ ItineraryAttractionRecord ] = field( default_factory=list )
   transportation_rows: list[ ItineraryTransportationRecord ] = field(
      default_factory=list )
   guardians_talk_rows: list[ ItineraryGuardiansTalkRecord ] = field( default_factory=list )
   wild_encounter_rows: list[ ItineraryWildEncounterRecord ] = field( default_factory=list )
   event_rows: list[ ItineraryEventRecord ] = field( default_factory=list )


   def is_empty( self ) -> bool:
      return self.date_value == None


   def itinerary_date( self ) -> date:
      return DateValues.parse_date_value( self.date_value )


   def month( self ) -> int:
      return self.itinerary_date().month


   def day( self ) -> int:
      return self.itinerary_date().day


   def year( self ) -> int:
      return self.itinerary_date().year


   def species_exhibit_pairs( self ) -> list[ SpeciesExhibitKey ]:
      return [
         animal.species_exhibit_key()
         for animal in self.animal_rows
      ]


   def attraction_names( self ) -> list[ str ]:
      return [
         attraction.attraction
         for attraction in self.attraction_rows
      ]


   def transportation_names( self ) -> list[ str ]:
      return [
         transportation.transportation
         for transportation in self.transportation_rows
      ]


   def guardians_talk_names( self ) -> list[ str ]:
      return [
         talk.talk_name
         for talk in self.guardians_talk_rows
      ]


   def wild_encounter_names( self ) -> list[ str ]:
      return [
         encounter.wild_encounter
         for encounter in self.wild_encounter_rows
      ]
