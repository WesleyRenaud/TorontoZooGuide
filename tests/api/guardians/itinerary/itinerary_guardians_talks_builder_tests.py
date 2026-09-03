from __future__ import annotations

from api.guardians.itinerary.itinerary_guardians_talks_builder import ItineraryGuardiansTalksBuilder
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.models.guardians_talk import GuardiansTalk


LION_TALK = 'Lion Talk'
ZEBRA_TALK = 'Zebra Talk'
SAVED_START = '11:00 AM'
SAVED_END = '11:30 AM'


def _guardians_talk(
      name: str,
      *,
      start_time: str | None = None,
      end_time: str | None = None,
      is_deleted: bool = False ) -> GuardiansTalk:
   return GuardiansTalk(
      name=name,
      location='Talk Circle',
      x_coord=1.0,
      y_coord=2.0,
      start_time=start_time,
      end_time=end_time,
      is_deleted=is_deleted )


def _saved_guardians_talk(
      *,
      talk_name: str,
      start_time: str | None = None,
      end_time: str | None = None,
      is_deleted: bool = False ) -> ItineraryGuardiansTalkRecord:
   return ItineraryGuardiansTalkRecord(
      talk_name=talk_name,
      start_time=start_time,
      end_time=end_time,
      is_deleted=is_deleted )


def Test_Build_TestMatchingSaved_ExpectTimesAndDeletedCopied() -> None:
   talks = [ _guardians_talk( LION_TALK ) ]
   saved = [
      _saved_guardians_talk(
         talk_name=LION_TALK,
         start_time=SAVED_START,
         end_time=SAVED_END,
         is_deleted=True ),
   ]

   result = ItineraryGuardiansTalksBuilder.build( talks, saved )

   assert result[ 0 ].start_time == SAVED_START
   assert result[ 0 ].end_time == SAVED_END
   assert result[ 0 ].is_deleted is True


def Test_Build_TestNoMatch_ExpectUnchanged() -> None:
   talks = [
      _guardians_talk(
         ZEBRA_TALK,
         start_time='10:00 AM',
         end_time='10:20 AM',
         is_deleted=False ),
   ]
   saved = [
      _saved_guardians_talk(
         talk_name=LION_TALK,
         start_time=SAVED_START,
         end_time=SAVED_END,
         is_deleted=True ),
   ]

   result = ItineraryGuardiansTalksBuilder.build( talks, saved )

   assert result[ 0 ].name == ZEBRA_TALK
   assert result[ 0 ].start_time == '10:00 AM'
   assert result[ 0 ].end_time == '10:20 AM'
   assert result[ 0 ].is_deleted is False


def Test_Build_TestSortsByNameAndStartTime_ExpectOrdered() -> None:
   talks = [
      _guardians_talk( ZEBRA_TALK, start_time='2:00 PM' ),
      _guardians_talk( LION_TALK, start_time='1:00 PM' ),
      _guardians_talk( LION_TALK, start_time='11:00 AM' ),
   ]

   result = ItineraryGuardiansTalksBuilder.build( talks, [] )

   assert [ ( talk.name, talk.start_time ) for talk in result ] == [
      ( LION_TALK, '11:00 AM' ),
      ( LION_TALK, '1:00 PM' ),
      ( ZEBRA_TALK, '2:00 PM' ),
   ]
