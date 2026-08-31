from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.unscheduling.guardians_talk_unschedule_preparer import GuardiansTalkUnschedulePreparer
from api.models.animal_diff import AnimalDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.itinerary_event import ItineraryEvent
from api.shared.enums import ItineraryEventType


ZEBRA_TALK = "Grevy's Zebra"
LION_TALK = 'African Lion'


def _empty_saved() -> SavedItinerary:
   return SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )


def Test_TimeBlocks_TestTimedTalk_ExpectTimeBlock() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )

   assert GuardiansTalkUnschedulePreparer.time_blocks( [ talk ] ) == [
      TimeBlock( start_seconds=12 * 3600, end_seconds=12 * 3600 + 30 * 60 ),
   ]


def Test_NewlyAddedActive_TestNewTimedTalk_ExpectTalk() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )

   assert GuardiansTalkUnschedulePreparer.newly_added_active(
      _empty_saved(),
      [ talk ] ) == [ talk ]


def Test_NewlyAddedActive_TestAlreadySavedOrDeletedOrUntimed_ExpectEmpty() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name=ZEBRA_TALK,
            start_time='12:00 PM',
            end_time='12:30 PM',
            is_deleted=False ),
      ],
   )
   talks = [
      GuardiansTalkDiff(
         name=ZEBRA_TALK,
         is_deleted=False,
         start_time='12:00 PM',
         end_time='12:30 PM' ),
      GuardiansTalkDiff(
         name=LION_TALK,
         is_deleted=True,
         start_time='1:00 PM',
         end_time='1:30 PM' ),
      GuardiansTalkDiff(
         name='Slender-Tailed Meerkat',
         is_deleted=False,
         start_time=None,
         end_time=None ),
   ]

   assert GuardiansTalkUnschedulePreparer.newly_added_active( saved, talks ) == []


def Test_SavedItineraryHasOverlap_TestOverlappingAnimal_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='12:00 PM',
            end_time='12:08 PM' ),
      ],
   )
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )

   assert GuardiansTalkUnschedulePreparer.saved_itinerary_has_overlap( saved, [ talk ] )


def Test_PrepareValidatedForReschedule_TestClearsListedSchedulesAndOverlappingEvents() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM' ),
      ],
      attractions=[],
      guardians_talks=[ talk ],
      wild_encounters=[],
      events=[
         ItineraryEvent(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM' ),
         ItineraryEvent(
            event_type=ItineraryEventType.LUNCH,
            start_time='2:00 PM',
            end_time='2:30 PM' ),
      ],
   )

   prepared = GuardiansTalkUnschedulePreparer.prepare_validated_for_reschedule(
      validated,
      [ talk ] )

   assert prepared.animals[ 0 ].start_time is None
   assert prepared.animals[ 0 ].end_time is None
   assert [
      ( event.event_type, event.start_time )
      for event in prepared.events
   ] == [
      ( ItineraryEventType.LUNCH, '2:00 PM' ),
   ]
