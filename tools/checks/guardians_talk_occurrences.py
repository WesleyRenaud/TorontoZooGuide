from __future__ import annotations

from datetime import date

from api.guardians.data_access.guardians_talk_occurrence_record import GuardiansTalkOccurrenceRecord
from api.models import ScheduledOccurrence
from .guardians_talk_listing import GuardiansTalkListing


class GuardiansTalkOccurrences():
   by_listing: dict[ GuardiansTalkListing, set[ GuardiansTalkOccurrenceRecord ] ]


   def __init__( self ) -> None:
      self.by_listing = {}


   def add(
         self,
         listing: GuardiansTalkListing,
         scheduled_date: date,
         talk_time: str ) -> None:
      self.by_listing.setdefault( listing, set() ).add(
         GuardiansTalkOccurrenceRecord(
            occurrence_date=scheduled_date.isoformat(),
            talk_time=talk_time,
         )
      )


   def add_listing( self, listing: GuardiansTalkListing ) -> None:
      self.by_listing.setdefault( listing, set() )


   def add_scheduled(
         self,
         listing: GuardiansTalkListing,
         scheduled: list[ ScheduledOccurrence ] ) -> None:
      for occurrence in scheduled:
         self.add(
            listing,
            date.fromisoformat( occurrence.date ),
            occurrence.time,
         )


   def listings( self ) -> set[ GuardiansTalkListing ]:
      return set( self.by_listing )


   def for_listing( self, listing: GuardiansTalkListing ) -> set[ GuardiansTalkOccurrenceRecord ]:
      return self.by_listing.get( listing, set() )
