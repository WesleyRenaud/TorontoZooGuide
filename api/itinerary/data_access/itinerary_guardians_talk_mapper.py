from ... import zoo
from .itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord


def map_itinerary_guardians_talk_record( row ):
   return ItineraryGuardiansTalkRecord(
      talk_name=row[ 'TALK_NAME' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ],
      is_deleted=zoo.ZooUtil.as_boolean( row[ 'IS_DELETED' ] ) )


def map_itinerary_guardians_talk_records( rows ):
   return [
      map_itinerary_guardians_talk_record( row )
      for row in rows
   ]
