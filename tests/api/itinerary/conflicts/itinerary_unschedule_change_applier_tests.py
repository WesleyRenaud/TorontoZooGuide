from __future__ import annotations

from api.itinerary.conflicts.itinerary_unschedule_change_applier import ItineraryUnscheduleChangeApplier
from api.itinerary.conflicts.itinerary_unschedule_requirements import ItineraryUnscheduleRequirements
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.models.animal_diff import AnimalDiff
from api.models.attraction_diff import AttractionDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.itinerary_event import ItineraryEvent
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryEventType


def _validated_with_scheduled_guest_items() -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=100,
            new_likelihood=100,
            start_time='2:30 PM',
            end_time='2:45 PM' ),
      ],
      attractions=[
         AttractionDiff(
            name='Conservation Carousel',
            old_likelihood=100,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:15 AM' ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      events=[
         ItineraryEvent(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM' ),
      ],
   )


def Test_Apply_TestNoRequirements_ExpectUnchangedValidated() -> None:
   validated = _validated_with_scheduled_guest_items()

   result = ItineraryUnscheduleChangeApplier.apply(
      validated,
      ItineraryUnscheduleRequirements( talks=[], encounters=[] ) )

   assert result is validated
   assert result.animals[ 0 ].start_time == '2:30 PM'
   assert result.attractions[ 0 ].start_time == '11:00 AM'
   assert len( result.events ) == 1


def Test_Apply_TestEncounterOverlap_ExpectGuestSchedulesCleared() -> None:
   validated = _validated_with_scheduled_guest_items()
   requirements = ItineraryUnscheduleRequirements(
      talks=[],
      encounters=[
         WildEncounterDiff(
            name='Guardians of White Rhinos',
            is_deleted=False,
            start_time='2:00 PM',
            end_time='2:45 PM',
            meeting_spot='Wild Encounter - Africa Meeting Spot',
            link='https://example.com/rhino' ),
      ],
   )

   result = ItineraryUnscheduleChangeApplier.apply( validated, requirements )

   assert result.animals[ 0 ].start_time is None
   assert result.animals[ 0 ].end_time is None
   assert result.attractions[ 0 ].start_time is None
   assert result.attractions[ 0 ].end_time is None
   assert len( result.events ) == 1


def Test_Apply_TestTalkOverlap_ExpectGuestSchedulesCleared() -> None:
   validated = _validated_with_scheduled_guest_items()
   requirements = ItineraryUnscheduleRequirements(
      talks=[
         GuardiansTalkDiff(
            name='Nile Soft-Shelled Turtle',
            is_deleted=False,
            start_time='12:00 PM',
            end_time='12:30 PM',
            location='African Rainforest Pavilion' ),
      ],
      encounters=[],
   )

   result = ItineraryUnscheduleChangeApplier.apply( validated, requirements )

   assert result.animals[ 0 ].start_time is None
   assert result.attractions[ 0 ].start_time is None
   assert result.events == []
