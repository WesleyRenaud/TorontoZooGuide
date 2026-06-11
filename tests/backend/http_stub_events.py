from __future__ import annotations

from typing import Any

from http_support_constants import GUARDIANS_TALK_LOCATION
from http_support_constants import GUARDIANS_TALK_NAME
from http_support_constants import WILD_ENCOUNTER_LINK
from http_support_constants import WILD_ENCOUNTER_MEETING_SPOT
from http_support_constants import WILD_ENCOUNTER_NAME

from api.models import GuardiansTalk
from api.models import ScheduledOccurrence
from api.models import WildEncounter

class EventsStubMixin:
   def get_guardians_talk_schedule( self, **kwargs: Any ) -> list[ GuardiansTalk ]:
         self.calls.append( ( 'get_guardians_talk_schedule', kwargs ) )
         return [ GuardiansTalk( name=GUARDIANS_TALK_NAME, location=GUARDIANS_TALK_LOCATION, x_coord=51.138, y_coord=41.279 ) ]


   def get_available_wild_encounters( self, **kwargs: Any ) -> list[ WildEncounter ]:
         self.calls.append( ( 'get_available_wild_encounters', kwargs ) )
         return [
            WildEncounter(
               name=WILD_ENCOUNTER_NAME,
               meeting_spot=WILD_ENCOUNTER_MEETING_SPOT,
               link=WILD_ENCOUNTER_LINK )
         ]


   def get_guardians_talks_matching_query( self, **kwargs: Any ) -> list[ GuardiansTalk ]:
         self.calls.append( ( 'get_guardians_talks_matching_query', kwargs ) )
         return [ GuardiansTalk( name=GUARDIANS_TALK_NAME, location=GUARDIANS_TALK_LOCATION, x_coord=51.138, y_coord=41.279 ) ]


   def get_wild_encounters_matching_query( self, **kwargs: Any ) -> list[ WildEncounter ]:
         self.calls.append( ( 'get_wild_encounters_matching_query', kwargs ) )
         return [
            WildEncounter(
               name=WILD_ENCOUNTER_NAME,
               meeting_spot=WILD_ENCOUNTER_MEETING_SPOT,
               link=WILD_ENCOUNTER_LINK )
         ]


   def get_guardians_talk_locations( self ) -> list[ str ]:
         self.calls.append( ( 'get_guardians_talk_locations', {} ) )
         return [ GUARDIANS_TALK_LOCATION ]


   def get_guardians_talk_names( self ) -> list[ str ]:
         self.calls.append( ( 'get_guardians_talk_names', {} ) )
         return [ GUARDIANS_TALK_NAME ]


   def get_guardians_talk_names_at_location( self, location: str ) -> list[ str ]:
         self.calls.append( ( 'get_guardians_talk_names_at_location', { 'location': location } ) )
         return [ GUARDIANS_TALK_NAME ]


   def get_guardians_talk_occurrences( self, **kwargs: Any ) -> list[ ScheduledOccurrence ]:
         self.calls.append( ( 'get_guardians_talk_occurrences', kwargs ) )
         return [
            ScheduledOccurrence(
               date='2026-06-15',
               time='10:00' )
         ]


   def get_wild_encounter_names( self ) -> list[ str ]:
         self.calls.append( ( 'get_wild_encounter_names', {} ) )
         return [ WILD_ENCOUNTER_NAME ]


   def get_wild_encounter_occurrences( self, **kwargs: Any ) -> list[ ScheduledOccurrence ]:
         self.calls.append( ( 'get_wild_encounter_occurrences', kwargs ) )
         return [
            ScheduledOccurrence(
               date='2026-06-15',
               time='14:00' )
         ]
