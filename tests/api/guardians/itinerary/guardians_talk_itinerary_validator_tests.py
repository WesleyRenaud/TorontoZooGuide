from __future__ import annotations

from api.guardians.itinerary.guardians_talk_itinerary_validator import GuardiansTalkItineraryValidator
from api.itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from api.models import GuardiansTalk


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


def Test_ValidateForItinerary_TestAvailableAndUnavailable_ExpectSplitDiffs() -> None:
   day_schedule = [
      GuardiansTalk(
         name='African Lion',
         location='Africa Savanna',
         x_coord=51.138,
         y_coord=41.279,
         start_time='10:00 AM',
         maximum_duration=30,
         is_available=True ),
   ]

   result = GuardiansTalkItineraryValidator.validate_for_itinerary(
      guardians_talks_to_include=[
         ItineraryGuardiansTalkInput( name='African Lion', start_time='10:00' ),
         ItineraryGuardiansTalkInput( name='Amur Tiger', start_time='10:00' ),
      ],
      day_schedule=day_schedule )

   assert [
      ( d.name, d.is_deleted, d.start_time, d.end_time )
      for d in result
   ] == [
      ( 'African Lion', False, '10:00', '10:30 AM' ),
      ( 'Amur Tiger', True, '10:00', None ),
   ]
