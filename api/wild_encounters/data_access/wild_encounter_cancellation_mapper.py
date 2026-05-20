from .wild_encounter_cancellation_record import WildEncounterCancellationRecord


def map_wild_encounter_cancellation_record( row ):
   return WildEncounterCancellationRecord(
      cancellation_date=row[ 'CANCELLATION_DATE' ],
      encounter_time=row[ 'ENCOUNTER_TIME' ] )


def map_wild_encounter_cancellation_records( rows ):
   return [
      map_wild_encounter_cancellation_record( row )
      for row in rows
   ]
