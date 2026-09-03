from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.unscheduling.fixed_time_activity_unschedule_preparer import FixedTimeActivityUnschedulePreparer
from api.models.animal_diff import AnimalDiff
from api.models.attraction_diff import AttractionDiff
from api.models.itinerary_event import ItineraryEvent
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.models.transportation_diff import TransportationDiff
from api.shared.enums import ItineraryEventType
from api.types import Types

def Test_OverlapsAnyTimeBlock_TestOverlappingTimes_ExpectTrue() -> None:
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert FixedTimeActivityUnschedulePreparer.overlaps_any_time_block(
      '10:15 AM',
      '10:45 AM',
      blocks )


def Test_OverlapsAnyTimeBlock_TestAdjacentTimes_ExpectFalse() -> None:
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert not FixedTimeActivityUnschedulePreparer.overlaps_any_time_block(
      '10:30 AM',
      '11:00 AM',
      blocks )


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
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert FixedTimeActivityUnschedulePreparer.saved_itinerary_has_overlap( saved, blocks )


def Test_SavedItineraryHasOverlap_TestNoOverlap_ExpectFalse() -> None:
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
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=13 * 3600, end_seconds=13 * 3600 + 30 * 60 ),
   ]

   assert not FixedTimeActivityUnschedulePreparer.saved_itinerary_has_overlap( saved, blocks )


def Test_PrepareValidatedForReschedule_TestActivityBlocks_ExpectClearedGuestSchedules() -> None:
   validated = ValidatedItinerary(
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
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[
         ItineraryEvent(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=14 * 3600, end_seconds=14 * 3600 + 45 * 60 ),
   ]

   result = FixedTimeActivityUnschedulePreparer.prepare_validated_for_reschedule(
      validated,
      blocks )

   assert result.animals[ 0 ].start_time is None
   assert result.animals[ 0 ].end_time is None
   assert len( result.events ) == 1


def Test_OverlapsAnyTimeBlock_TestInvalidScheduleTimes_ExpectFalse() -> None:
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert not FixedTimeActivityUnschedulePreparer.overlaps_any_time_block(
      None,
      None,
      blocks )


def Test_SavedItineraryHasOverlap_TestOverlappingAttraction_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:15 AM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert FixedTimeActivityUnschedulePreparer.saved_itinerary_has_overlap( saved, blocks )


def Test_SavedItineraryHasOverlap_TestOverlappingTransportation_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False,
            start_time='10:00 AM',
            end_time='10:20 AM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert FixedTimeActivityUnschedulePreparer.saved_itinerary_has_overlap( saved, blocks )


def Test_SavedItineraryHasOverlap_TestOverlappingEvent_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      event_rows=[
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='10:00 AM',
            end_time='10:30 AM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert FixedTimeActivityUnschedulePreparer.saved_itinerary_has_overlap( saved, blocks )


def Test_PrepareValidatedForReschedule_TestAttractionAndTransportation_ExpectCleared() -> None:
   validated = ValidatedItinerary(
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animals=[],
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
      events=[],
      transportations=[
         TransportationDiff(
            name='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            start_time='1:00 PM',
            end_time='1:30 PM',
            legs=[
               ItineraryTransportationLeg(
                  from_station='A',
                  to_station='B',
                  start_time='1:00 PM',
                  end_time='1:30 PM',
                  transportation='Zoomobile',
                  added_as_attraction=False ),
            ],
            added_as_attraction=False ),
      ],
   )

   result = FixedTimeActivityUnschedulePreparer.prepare_validated_for_reschedule(
      validated,
      [] )

   assert result.attractions[ 0 ].start_time is None
   assert result.attractions[ 0 ].end_time is None
   assert result.transportations[ 0 ].start_time is None
   assert result.transportations[ 0 ].end_time is None
   assert result.transportations[ 0 ].legs == []


def Test_RemoveOverlappingEvents_TestLunchOverlaps_ExpectLunchRemoved() -> None:
   validated = ValidatedItinerary(
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[
         ItineraryEvent(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM' ),
         ItineraryEvent(
            event_type=ItineraryEventType.ARRIVAL,
            start_time='9:00 AM',
            end_time='9:15 AM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=12 * 3600, end_seconds=12 * 3600 + 45 * 60 ),
   ]

   FixedTimeActivityUnschedulePreparer.remove_overlapping_events( validated, blocks )

   assert [ event.event_type for event in validated.events ] == [ ItineraryEventType.ARRIVAL ]


def Test_ClearOverlappingSavedSchedules_TestAllRowKinds_ExpectClearCalls(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls: list[ str ] = []

   monkeypatch.setattr(
      UnscheduleItineraryItemProvider,
      'clear_itinerary_animal_schedule',
      lambda cur, **kwargs: calls.append( 'animal' ) )
   monkeypatch.setattr(
      UnscheduleItineraryItemProvider,
      'clear_itinerary_attraction_schedule',
      lambda cur, **kwargs: calls.append( 'attraction' ) )
   monkeypatch.setattr(
      UnscheduleItineraryItemProvider,
      'clear_itinerary_transportation_schedule',
      lambda cur, **kwargs: calls.append( 'transportation' ) )
   monkeypatch.setattr(
      UnscheduleItineraryItemProvider,
      'delete_itinerary_event_schedule',
      lambda cur, **kwargs: calls.append( 'event' ) )

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
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:10 AM',
            end_time='10:20 AM' ),
      ],
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False,
            start_time='10:15 AM',
            end_time='10:45 AM' ),
      ],
      event_rows=[
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='10:00 AM',
            end_time='10:30 AM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=11 * 3600 ),
   ]
   cursor: Types.Cursor = object()

   FixedTimeActivityUnschedulePreparer.clear_overlapping_saved_schedules(
      cursor,
      saved,
      blocks )

   assert calls == [ 'animal', 'attraction', 'transportation', 'event' ]
