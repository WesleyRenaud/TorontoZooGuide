from .guardians_talk_schedule_record import GuardiansTalkScheduleRecord


def map_guardians_talk_schedule_record( row ):
   return GuardiansTalkScheduleRecord(
      name=row[ 'NAME' ],
      location=row[ 'LOCATION' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ],
      maximum_duration=row[ 'MAXIMUM_DURATION' ],
      schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
      schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
      monday_time=row[ 'MONDAY_TIME' ],
      tuesday_time=row[ 'TUESDAY_TIME' ],
      wednesday_time=row[ 'WEDNESDAY_TIME' ],
      thursday_time=row[ 'THURSDAY_TIME' ],
      friday_time=row[ 'FRIDAY_TIME' ],
      saturday_time=row[ 'SATURDAY_TIME' ],
      sunday_time=row[ 'SUNDAY_TIME' ] )



def map_guardians_talk_schedule_records( rows ):
   return [
      map_guardians_talk_schedule_record( row )
      for row in rows
   ]
