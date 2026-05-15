from .meet_the_guardians_talk_record import MeetTheGuardiansTalkRecord


def map_meet_the_guardians_talk_record( row ):
   return MeetTheGuardiansTalkRecord(
      name=row[ 'NAME' ],
      location=row[ 'LOCATION' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ],
      maximum_duration=row[ 'MAXIMUM_DURATION' ] )



def map_meet_the_guardians_talk_records( rows ):
   return [
      map_meet_the_guardians_talk_record( row )
      for row in rows
   ]
