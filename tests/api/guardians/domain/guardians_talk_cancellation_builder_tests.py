from __future__ import annotations

from api.guardians.cancellations.guardians_talk_cancellation_builder import GuardiansTalkCancellationBuilder


TALK_NAME = 'African Lion'
TALK_LOCATION = 'Africa Savanna'
CANCELLATION_DATE = '2026-06-15'
TALK_TIME = '10:00 AM'


def Test_Build_TestTalkCancellation_ExpectMapsFields() -> None:
   cancellation = GuardiansTalkCancellationBuilder.build(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      date=CANCELLATION_DATE,
      time=TALK_TIME )

   assert cancellation.talk_name == TALK_NAME
   assert cancellation.location == TALK_LOCATION
   assert cancellation.cancellation_date == CANCELLATION_DATE
   assert cancellation.talk_time == TALK_TIME
