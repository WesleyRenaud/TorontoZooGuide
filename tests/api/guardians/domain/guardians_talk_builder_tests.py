from __future__ import annotations

from api.guardians.data_access.meet_the_guardians_talk_record import MeetTheGuardiansTalkRecord
from api.guardians.domain.guardians_talk_builder import GuardiansTalkBuilder


STATION_COORD = 0.0


def _talk_record( *, name: str, location: str ) -> MeetTheGuardiansTalkRecord:
   return MeetTheGuardiansTalkRecord(
      name=name,
      location=location,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      maximum_duration=30 )


def Test_BuildDetails_TestNoIncludeFilter_ExpectAllTalksSorted() -> None:
   talks = GuardiansTalkBuilder.build_details( [
      _talk_record( name='Zebra Talk', location='Africa Savanna' ),
      _talk_record( name='African Lion', location='Africa Savanna' ),
   ] )

   assert [ ( talk.name, talk.location ) for talk in talks ] == [
      ( 'African Lion', 'Africa Savanna' ),
      ( 'Zebra Talk', 'Africa Savanna' ),
   ]


def Test_BuildDetails_TestIncludeFilter_ExpectMatchingTalkOnly() -> None:
   talks = GuardiansTalkBuilder.build_details(
      [
         _talk_record( name='African Lion', location='Africa Savanna' ),
         _talk_record( name='Zebra Talk', location='Africa Savanna' ),
      ],
      guardians_talks_to_include=[ 'african lion' ] )

   assert [ talk.name for talk in talks ] == [ 'African Lion' ]


def Test_BuildDetails_TestEmptyIncludeList_ExpectNoTalks() -> None:
   talks = GuardiansTalkBuilder.build_details(
      [ _talk_record( name='African Lion', location='Africa Savanna' ) ],
      guardians_talks_to_include=[] )

   assert talks == []
