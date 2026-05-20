from .guardians_talk_cancellation_record import GuardiansTalkCancellationRecord


def map_guardians_talk_cancellation_record( row ):
   return GuardiansTalkCancellationRecord(
      cancellation_date=row[ 'CANCELLATION_DATE' ],
      talk_time=row[ 'TALK_TIME' ] )


def map_guardians_talk_cancellation_records( rows ):
   return [
      map_guardians_talk_cancellation_record( row )
      for row in rows
   ]
