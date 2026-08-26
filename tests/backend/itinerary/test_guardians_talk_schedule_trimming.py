from api.guardians.itinerary.guardians_talk_itinerary_validator import GuardiansTalkItineraryValidator
from api.itinerary.scheduling.unscheduling.guardians_talk_schedule_trimming import apply_guardians_talk_trimming
from api.models import GuardiansTalk
from api.models import WildEncounter
from api.wild_encounters.itinerary.wild_encounter_itinerary_validator import WildEncounterItineraryValidator


def test_build_guardians_talk_diff_preserves_saved_times_when_talk_not_on_schedule() -> None:
   talk = GuardiansTalkItineraryValidator.build_diff_for_visit_day(
      'Spotted Hyena',
      None,
      start_time_override='13:00',
      end_time_override='13:30',
   )

   assert talk.is_deleted is True
   assert talk.start_time == '13:00'
   assert talk.end_time == '13:30'


def test_apply_guardians_talk_trimming_keeps_tail_after_wild_encounter() -> None:
   encounter = WildEncounterItineraryValidator.build_diff_for_visit_day(
      'Grizzly Bear',
      WildEncounter(
         name='Grizzly Bear',
         meeting_spot='Spot',
         link='',
         start_time='13:00',
         maximum_duration=45,
         is_available=True,
      ),
   )
   talk = GuardiansTalkItineraryValidator.build_diff_for_visit_day(
      'African Lion',
      GuardiansTalk(
         name='African Lion',
         location='Africa Savanna',
         x_coord=0,
         y_coord=0,
         start_time='13:30',
         maximum_duration=30,
         is_available=True,
      ),
   )

   trimmed_talks = apply_guardians_talk_trimming( [ talk ], [ encounter ] )

   assert trimmed_talks[ 0 ].start_time == '1:45 PM'
   assert trimmed_talks[ 0 ].end_time == '2:00 PM'


def test_apply_guardians_talk_trimming_gives_earlier_talk_precedence() -> None:
   first_talk = GuardiansTalkItineraryValidator.build_diff_for_visit_day(
      'African Lion',
      GuardiansTalk(
         name='African Lion',
         location='Africa Savanna',
         x_coord=0,
         y_coord=0,
         start_time='13:30',
         maximum_duration=30,
         is_available=True,
      ),
   )
   second_talk = GuardiansTalkItineraryValidator.build_diff_for_visit_day(
      'Amur Tiger',
      GuardiansTalk(
         name='Amur Tiger',
         location='Eurasia Wilds',
         x_coord=0,
         y_coord=0,
         start_time='13:45',
         maximum_duration=30,
         is_available=True,
      ),
   )

   trimmed_talks = apply_guardians_talk_trimming(
      [ first_talk, second_talk ],
      [],
   )

   assert trimmed_talks[ 0 ].start_time == '1:30 PM'
   assert trimmed_talks[ 0 ].end_time == '2:00 PM'
   assert trimmed_talks[ 1 ].start_time == '2:00 PM'
   assert trimmed_talks[ 1 ].end_time == '2:15 PM'
