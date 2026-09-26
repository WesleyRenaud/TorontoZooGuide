from __future__ import annotations

from dataclasses import dataclass

from ...models.attraction_diff import AttractionDiff
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ...shared.enums import ItinerarySaveIssueItemType
from ...shared.enums import ItineraryVisitWindowOverflowEnd
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
   overflow_end: ItineraryVisitWindowOverflowEnd | None = None


   @classmethod
   def from_wild_encounter_diff(
         issue_item_type: type[ 'ItinerarySaveIssueItem' ],
         wild_encounter: WildEncounterDiff,
         *,
         overflow_end: ItineraryVisitWindowOverflowEnd | None = None
         ) -> 'ItinerarySaveIssueItem':
      return issue_item_type(
         name=wild_encounter.name,
         start_time=wild_encounter.start_time,
         end_time=wild_encounter.end_time,
         item_type=ItinerarySaveIssueItemType.WILD_ENCOUNTER,
         meeting_spot=wild_encounter.meeting_spot or '',
         link=wild_encounter.link or '',
         overflow_end=overflow_end )


   @classmethod
   def from_guardians_talk_diff(
         issue_item_type: type[ 'ItinerarySaveIssueItem' ],
         guardians_talk: GuardiansTalkDiff,
         *,
         overflow_end: ItineraryVisitWindowOverflowEnd | None = None
         ) -> 'ItinerarySaveIssueItem':
      return issue_item_type(
         name=guardians_talk.name,
         start_time=guardians_talk.start_time,
         end_time=guardians_talk.end_time,
         item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
         location=guardians_talk.location or '',
         overflow_end=overflow_end )


   @classmethod
   def from_attraction_diff(
         issue_item_type: type[ 'ItinerarySaveIssueItem' ],
         attraction: AttractionDiff,
         *,
         overflow_end: ItineraryVisitWindowOverflowEnd | None = None
         ) -> 'ItinerarySaveIssueItem':
      return issue_item_type(
         name=attraction.name,
         start_time=attraction.start_time,
         end_time=attraction.end_time,
         item_type=ItinerarySaveIssueItemType.ATTRACTION,
         overflow_end=overflow_end )


   def to_dict( self ) -> dict[ str, str | None ]:
      return {
         'name': self.name,
         'start_time': self.start_time,
         'end_time': self.end_time,
         'item_type': self.item_type,
         'meeting_spot': self.meeting_spot,
         'location': self.location,
         'link': self.link,
         'overflow_end': (
            self.overflow_end.value if self.overflow_end is not None else None
         ),
      }
