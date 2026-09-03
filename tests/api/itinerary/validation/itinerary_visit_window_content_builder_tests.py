from __future__ import annotations

from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.validation.itinerary_visit_window_content_builder import ItineraryVisitWindowContentBuilder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryEventType


def Test_FilterGuardiansTalks_TestOutsideArrival_ExpectDropped() -> None:
   talks = [
      GuardiansTalkDiff(
         name="Grevy's Zebra",
         is_deleted=False,
         start_time='9:00 AM',
         end_time='9:30 AM' ),
      GuardiansTalkDiff(
         name='African Lion',
         is_deleted=False,
         start_time='11:00 AM',
         end_time='11:30 AM' ),
   ]

   kept = ItineraryVisitWindowContentBuilder.filter_guardians_talks(
      talks,
      arrival_time='10:00 AM',
      departure_time='5:00 PM' )

   assert [ talk.name for talk in kept ] == [ 'African Lion' ]


def Test_FilterWildEncounters_TestOutsideDeparture_ExpectDropped() -> None:
   encounters = [
      WildEncounterDiff(
         name='African Rainforest',
         is_deleted=False,
         start_time='11:00 AM',
         end_time='11:45 AM' ),
      WildEncounterDiff(
         name='Kangaroo',
         is_deleted=False,
         start_time='4:30 PM',
         end_time='5:15 PM' ),
   ]

   kept = ItineraryVisitWindowContentBuilder.filter_wild_encounters(
      encounters,
      arrival_time='10:00 AM',
      departure_time='5:00 PM' )

   assert [ encounter.name for encounter in kept ] == [ 'African Rainforest' ]


def Test_EventsFromSavedRows_TestSavedRows_ExpectSkipsArrivalDepartureAndOutsideWindow() -> None:
   events = ItineraryVisitWindowContentBuilder.events_from_saved_rows(
      [
         ItineraryEventRecord(
            event_type=ItineraryEventType.ARRIVAL,
            start_time='10:00 AM',
            end_time='10:00 AM' ),
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM' ),
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='5:30 PM',
            end_time='6:00 PM' ),
      ],
      arrival_time='10:00 AM',
      departure_time='5:00 PM' )

   assert [
      ( event.event_type, event.start_time, event.end_time )
      for event in events
   ] == [
      ( ItineraryEventType.LUNCH, '12:00 PM', '12:30 PM' ),
   ]
