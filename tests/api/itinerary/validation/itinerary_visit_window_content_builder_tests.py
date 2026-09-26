from __future__ import annotations

from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.validation.itinerary_visit_window_content_builder import ItineraryVisitWindowContentBuilder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryEventType
from api.shared.enums.position import Position


def Test_FilterGuardiansTalks_TestOutsideArrival_ExpectDropped() -> None:
   outside_talk = GuardiansTalkDiff(
      name="Grevy's Zebra",
      is_deleted=False,
      start_time='9:00 AM',
      end_time='9:30 AM' )
   inside_talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='11:00 AM',
      end_time='11:30 AM' )
   talks = [ outside_talk, inside_talk ]
   arrival_time = '10:00 AM'
   departure_time = '5:00 PM'

   kept = ItineraryVisitWindowContentBuilder.filter_guardians_talks(
      talks,
      arrival_time=arrival_time,
      departure_time=departure_time )

   assert [ talk.name for talk in kept ] == [ inside_talk.name ]


def Test_FilterWildEncounters_TestOutsideDeparture_ExpectDropped() -> None:
   inside_encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='11:00 AM',
      end_time='11:45 AM' )
   outside_encounter = WildEncounterDiff(
      name='Kangaroo',
      is_deleted=False,
      start_time='4:30 PM',
      end_time='5:15 PM' )
   encounters = [ inside_encounter, outside_encounter ]
   arrival_time = '10:00 AM'
   departure_time = '5:00 PM'

   kept = ItineraryVisitWindowContentBuilder.filter_wild_encounters(
      encounters,
      arrival_time=arrival_time,
      departure_time=departure_time )

   assert [ encounter.name for encounter in kept ] == [ inside_encounter.name ]


def Test_EventsFromSavedRows_TestSavedRows_ExpectSkipsArrivalDepartureAndOutsideWindow() -> None:
   arrival_time = '10:00 AM'
   departure_time = '5:00 PM'
   lunch = ItineraryEventRecord(
      event_type=ItineraryEventType.LUNCH,
      start_time='12:00 PM',
      end_time='12:30 PM' )
   rows = [
      ItineraryEventRecord(
         event_type=ItineraryEventType.ARRIVAL,
         start_time=arrival_time,
         end_time=arrival_time ),
      lunch,
      ItineraryEventRecord(
         event_type=ItineraryEventType.LUNCH,
         start_time='5:30 PM',
         end_time='6:00 PM' ),
   ]

   events = ItineraryVisitWindowContentBuilder.events_from_saved_rows(
      rows,
      arrival_time=arrival_time,
      departure_time=departure_time )

   assert [
      ( event.event_type, event.start_time, event.end_time )
      for event in events
   ] == [
      ( lunch.event_type, lunch.start_time, lunch.end_time ),
   ]
   assert events[ Position.FIRST ].event_type == lunch.event_type
