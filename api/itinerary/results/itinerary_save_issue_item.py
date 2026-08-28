from __future__ import annotations

from dataclasses import dataclass

from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ...shared.enums import ItinerarySaveIssueItemType
from ...types import Types


@dataclass( frozen=True )
class ItinerarySaveIssueItem:
   name: str
   start_time: Types.ScheduleTimeKey
   end_time: Types.ScheduleTimeKey
   item_type: str
   meeting_spot: str = ''
   location: str = ''
   link: str = ''


   @classmethod
   def from_wild_encounter_diff(
         issue_item_type: type[ 'ItinerarySaveIssueItem' ],
         wild_encounter: WildEncounterDiff ) -> 'ItinerarySaveIssueItem':
      return issue_item_type(
         name=wild_encounter.name,
         start_time=wild_encounter.start_time,
         end_time=wild_encounter.end_time,
         item_type=ItinerarySaveIssueItemType.WILD_ENCOUNTER,
         meeting_spot=wild_encounter.meeting_spot or '',
         link=wild_encounter.link or '' )


   @classmethod
   def from_guardians_talk_diff(
         issue_item_type: type[ 'ItinerarySaveIssueItem' ],
         guardians_talk: GuardiansTalkDiff ) -> 'ItinerarySaveIssueItem':
      return issue_item_type(
         name=guardians_talk.name,
         start_time=guardians_talk.start_time,
         end_time=guardians_talk.end_time,
         item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
         location=guardians_talk.location or '' )


   def to_dict( self ) -> dict[ str, str | None ]:
      return {
         'name': self.name,
         'start_time': self.start_time,
         'end_time': self.end_time,
         'item_type': self.item_type,
         'meeting_spot': self.meeting_spot,
         'location': self.location,
         'link': self.link,
      }
