from __future__ import annotations

from .guardians_talk_cancellation_input import GuardiansTalkCancellationInput
from ...types import Types


class GuardiansTalkCancellationBuilder():
   @classmethod
   def build(
         cls,
         talk: str,
         location: str,
         date: Types.DateKey,
         time: str ) -> GuardiansTalkCancellationInput:
      return GuardiansTalkCancellationInput(
         talk_name=talk,
         location=location,
         cancellation_date=date,
         talk_time=time )
