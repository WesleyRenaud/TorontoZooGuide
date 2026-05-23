from __future__ import annotations

from ...types import DateKey
from .guardians_talk_cancellation_input import GuardiansTalkCancellationInput


def build_guardians_talk_cancellation(
      talk: str,
      location: str,
      date: DateKey,
      time: str ) -> GuardiansTalkCancellationInput:
   return GuardiansTalkCancellationInput(
      talk_name=talk,
      location=location,
      cancellation_date=date,
      talk_time=time )
