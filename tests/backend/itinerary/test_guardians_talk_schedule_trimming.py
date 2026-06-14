from api.guardians.itinerary.guardians_talk_itinerary_validation import build_guardians_talk_diff_for_visit_day
from api.itinerary.scheduling.unscheduling.guardians_talk_schedule_trimming import apply_guardians_talk_trimming
from api.models import GuardiansTalk
from api.models import WildEncounter
from api.wild_encounters.logic.wild_encounter_itinerary_validation import build_wild_encounter_diff_for_visit_day


def test_apply_guardians_talk_trimming_keeps_tail_after_wild_encounter() -> None:
   encounter = build_wild_encounter_diff_for_visit_day(
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
   talk = build_guardians_talk_diff_for_visit_day(
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

   assert trimmed_talks[ 0 ].start_time == '13:45'
   assert trimmed_talks[ 0 ].end_time == '14:00'


def test_apply_guardians_talk_trimming_gives_earlier_talk_precedence() -> None:
   first_talk = build_guardians_talk_diff_for_visit_day(
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
   second_talk = build_guardians_talk_diff_for_visit_day(
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

   assert trimmed_talks[ 0 ].start_time == '13:30'
   assert trimmed_talks[ 0 ].end_time == '14:00'
   assert trimmed_talks[ 1 ].start_time == '14:00'
   assert trimmed_talks[ 1 ].end_time == '14:15'
