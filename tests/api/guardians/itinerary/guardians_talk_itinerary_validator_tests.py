from __future__ import annotations

from api.guardians.itinerary.guardians_talk_itinerary_validator import GuardiansTalkItineraryValidator
from api.itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from api.models.guardians_talk import GuardiansTalk


DAY_SCHEDULE = [
   GuardiansTalk(
      name='African Lion',
      location='Africa Savanna',
      x_coord=0.0,
      y_coord=0.0,
      start_time='10:00 AM',
      end_time='10:30 AM' ),
   GuardiansTalk(
      name='Amur Tiger',
      location='Eurasia Wilds',
      x_coord=1.0,
      y_coord=1.0,
      start_time='9:00 AM',
      end_time='9:30 AM' ),
]


def Test_ValidateForItinerary_TestCaseInsensitiveNames_ExpectSortedMatches() -> None:
   result = GuardiansTalkItineraryValidator.validate_for_itinerary(
      [
         ItineraryGuardiansTalkInput( name=' african lion ', start_time='10:00' ),
         ItineraryGuardiansTalkInput( name='AMUR TIGER', start_time='09:00' ),
      ],
      DAY_SCHEDULE )

   assert [ diff.name for diff in result if not diff.is_deleted ] == [
      'African Lion',
      'Amur Tiger',
   ]
