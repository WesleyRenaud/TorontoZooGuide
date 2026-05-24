from __future__ import annotations

from dataclasses import dataclass

from ...models.wild_encounter_diff import WildEncounterDiff
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItinerarySaveIssueItem:
   name: str
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
   meeting_spot: str
   link: str


   @classmethod
   def from_wild_encounter_diff(
         issue_item_type: type[ 'ItinerarySaveIssueItem' ],
         wild_encounter: WildEncounterDiff ) -> 'ItinerarySaveIssueItem':
      return issue_item_type(
         name=wild_encounter.name,
         start_time=wild_encounter.start_time,
         end_time=wild_encounter.end_time,
         meeting_spot=wild_encounter.meeting_spot,
         link=wild_encounter.link )


   def to_dict( self ) -> dict[ str, str | None ]:
      return {
         'name': self.name,
         'start_time': self.start_time,
         'end_time': self.end_time,
         'meeting_spot': self.meeting_spot,
         'link': self.link,
      }
