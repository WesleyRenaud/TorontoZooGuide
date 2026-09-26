from __future__ import annotations

from api.itinerary.conflicts.visit_window_overflow_issue_finder import VisitWindowOverflowIssueFinder
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.models.attraction_diff import AttractionDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType
from api.shared.enums import ItineraryVisitWindowOverflowEnd
from api.shared.enums.position import Position


ARRIVAL_TIME = '11:00 AM'
DEPARTURE_TIME = '1:00 PM'
TALK_NAME = 'African Lion'
ENCOUNTER_NAME = 'African Rainforest'
ATTRACTION_NAME = 'Splash Island'


def _talk(
      *,
      start_time: str,
      end_time: str,
      is_deleted: bool = False ) -> GuardiansTalkDiff:
   return GuardiansTalkDiff(
      name=TALK_NAME,
      is_deleted=is_deleted,
      start_time=start_time,
      end_time=end_time,
      location='Africa Savanna' )


def _find(
      arrival_time: str | None,
      departure_time: str | None,
      *,
      talks: list[ GuardiansTalkDiff ] | None = None,
      encounters: list[ WildEncounterDiff ] | None = None,
      attractions: list[ AttractionDiff ] | None = None ) -> list[ ItineraryResultReason ]:
   return VisitWindowOverflowIssueFinder.find(
      arrival_time,
      departure_time,
      guardians_talks=talks or [],
      wild_encounters=encounters or [],
      attractions=attractions or [] )


def Test_Find_TestBlankArrival_ExpectEmpty() -> None:
   talk = _talk( start_time='10:00 AM', end_time='10:30 AM' )

   issues = _find( '', DEPARTURE_TIME, talks=[ talk ] )

   assert issues == []


def Test_Find_TestBlankDeparture_ExpectEmpty() -> None:
   talk = _talk( start_time='10:00 AM', end_time='10:30 AM' )

   issues = _find( ARRIVAL_TIME, None, talks=[ talk ] )

   assert issues == []


def Test_Find_TestExactBounds_ExpectEmpty() -> None:
   talk = _talk( start_time=ARRIVAL_TIME, end_time=DEPARTURE_TIME )

   issues = _find( ARRIVAL_TIME, DEPARTURE_TIME, talks=[ talk ] )

   assert issues == []


def Test_Find_TestBeforeArrivalOnly_ExpectBeforeArrival() -> None:
   talk = _talk( start_time='10:00 AM', end_time=ARRIVAL_TIME )

   issues = _find( ARRIVAL_TIME, DEPARTURE_TIME, talks=[ talk ] )

   issue = issues[ Position.FIRST ]
   item = issue.items[ Position.FIRST ]

   assert len( issues ) == 1
   assert issue.code == ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS
   assert item.name == TALK_NAME
   assert item.start_time == talk.start_time
   assert item.end_time == talk.end_time
   assert item.overflow_end == ItineraryVisitWindowOverflowEnd.ARRIVAL
   assert item.item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK


def Test_Find_TestAfterDepartureOnly_ExpectAfterDeparture() -> None:
   encounter = WildEncounterDiff(
      name=ENCOUNTER_NAME,
      is_deleted=False,
      start_time=DEPARTURE_TIME,
      end_time='1:30 PM',
      meeting_spot='Africa Meeting Spot' )

   issues = _find( ARRIVAL_TIME, DEPARTURE_TIME, encounters=[ encounter ] )

   item = issues[ Position.FIRST ].items[ Position.FIRST ]

   assert item.name == ENCOUNTER_NAME
   assert item.overflow_end == ItineraryVisitWindowOverflowEnd.DEPARTURE
   assert item.item_type == ItinerarySaveIssueItemType.WILD_ENCOUNTER


def Test_Find_TestPinchBothEnds_ExpectBothOverflowEnds() -> None:
   talk = _talk( start_time='10:00 AM', end_time='2:00 PM' )

   issues = _find( ARRIVAL_TIME, DEPARTURE_TIME, talks=[ talk ] )

   item = issues[ Position.FIRST ].items[ Position.FIRST ]

   assert item.overflow_end == ItineraryVisitWindowOverflowEnd.BOTH


def Test_Find_TestUnscheduledAttraction_ExpectEmpty() -> None:
   attraction = AttractionDiff(
      name=ATTRACTION_NAME,
      old_likelihood=None,
      new_likelihood=100 )

   issues = _find( ARRIVAL_TIME, DEPARTURE_TIME, attractions=[ attraction ] )

   assert issues == []


def Test_Find_TestTimedAttractionAfterDeparture_ExpectOverflow() -> None:
   attraction = AttractionDiff(
      name=ATTRACTION_NAME,
      old_likelihood=None,
      new_likelihood=100,
      start_time='12:30 PM',
      end_time='2:00 PM' )

   issues = _find( ARRIVAL_TIME, DEPARTURE_TIME, attractions=[ attraction ] )

   item = issues[ Position.FIRST ].items[ Position.FIRST ]

   assert item.name == ATTRACTION_NAME
   assert item.item_type == ItinerarySaveIssueItemType.ATTRACTION
   assert item.overflow_end == ItineraryVisitWindowOverflowEnd.DEPARTURE


def Test_Find_TestDeletedTalk_ExpectEmpty() -> None:
   talk = _talk(
      start_time='10:00 AM',
      end_time='10:30 AM',
      is_deleted=True )

   issues = _find( ARRIVAL_TIME, DEPARTURE_TIME, talks=[ talk ] )

   assert issues == []


def Test_Find_TestDeletedEncounter_ExpectEmpty() -> None:
   encounter = WildEncounterDiff(
      name=ENCOUNTER_NAME,
      is_deleted=True,
      start_time='10:00 AM',
      end_time='10:30 AM' )

   issues = _find( ARRIVAL_TIME, DEPARTURE_TIME, encounters=[ encounter ] )

   assert issues == []


def Test_Find_TestInvalidTimeRange_ExpectEmpty() -> None:
   talk = _talk( start_time='2:00 PM', end_time='1:00 PM' )

   issues = _find( ARRIVAL_TIME, DEPARTURE_TIME, talks=[ talk ] )

   assert issues == []


def Test_FindFromSavedItinerary_TestTalkBeforeArrival_ExpectOverflow() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name=TALK_NAME,
            start_time='10:00 AM',
            end_time='10:30 AM',
            is_deleted=False ),
      ],
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter=ENCOUNTER_NAME,
            start_time='12:00 PM',
            end_time='12:30 PM',
            is_deleted=False ),
      ],
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction=ATTRACTION_NAME,
            old_likelihood=None,
            new_likelihood=100,
            start_time=None,
            end_time=None ),
      ] )

   issues = VisitWindowOverflowIssueFinder.find_from_saved_itinerary(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      saved_itinerary )

   item = issues[ Position.FIRST ].items[ Position.FIRST ]

   assert len( issues[ Position.FIRST ].items ) == 1
   assert item.name == TALK_NAME
   assert item.overflow_end == ItineraryVisitWindowOverflowEnd.ARRIVAL
