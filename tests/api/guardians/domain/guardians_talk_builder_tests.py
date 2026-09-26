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
   zebra_talk = _talk_record( name='Zebra Talk', location='Africa Savanna' )
   african_lion = _talk_record( name='African Lion', location='Africa Savanna' )
   records = [ zebra_talk, african_lion ]

   talks = GuardiansTalkBuilder.build_details( records )

   assert [ ( talk.name, talk.location ) for talk in talks ] == [
      ( african_lion.name, african_lion.location ),
      ( zebra_talk.name, zebra_talk.location ),
   ]


def Test_BuildDetails_TestIncludeFilter_ExpectMatchingTalkOnly() -> None:
   african_lion = _talk_record( name='African Lion', location='Africa Savanna' )
   zebra_talk = _talk_record( name='Zebra Talk', location='Africa Savanna' )
   records = [ african_lion, zebra_talk ]
   include = [ african_lion.name.lower() ]

   talks = GuardiansTalkBuilder.build_details(
      records,
      guardians_talks_to_include=include )

   assert [ talk.name for talk in talks ] == [ african_lion.name ]


def Test_BuildDetails_TestEmptyIncludeList_ExpectNoTalks() -> None:
   african_lion = _talk_record( name='African Lion', location='Africa Savanna' )
   records = [ african_lion ]

   talks = GuardiansTalkBuilder.build_details(
      records,
      guardians_talks_to_include=[] )

   assert talks == []
