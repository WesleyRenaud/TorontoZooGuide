from __future__ import annotations

from ..occurrences.guardians_talk_occurrence_input import GuardiansTalkOccurrenceInput
from ...types import Types


class GuardiansTalkOccurrenceBuilder():
   @classmethod
   def build(
         cls,
         talk: str,
         location: str,
         date: Types.DateKey,
         time: str ) -> GuardiansTalkOccurrenceInput:
      return GuardiansTalkOccurrenceInput(
         talk_name=talk,
         location=location,
         occurrence_date=date,
         talk_time=time )
