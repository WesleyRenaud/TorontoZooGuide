from __future__ import annotations

from api.guardians.itinerary.guardians_talk_itinerary_validator import GuardiansTalkItineraryValidator


def Test_BuildDiffForVisitDay_TestMissingTalk_ExpectDeletedDiffWithOverrides() -> None:
   talk = GuardiansTalkItineraryValidator.build_diff_for_visit_day(
      'Spotted Hyena',
      None,
      start_time_override='13:00',
      end_time_override='13:30',
   )

   assert talk.is_deleted is True
   assert talk.start_time == '13:00'
   assert talk.end_time == '13:30'
