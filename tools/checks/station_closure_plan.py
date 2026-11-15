from __future__ import annotations

from datetime import date

from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from api.transportation.data_access.transportation_station_status_record import TransportationStationStatusRecord
from .station_change import StationChange
from .station_closure import StationClosure


class StationClosurePlan():
   added: list[ StationChange ]
   ended: list[ StationChange ]
   extended: list[ StationChange ]


   def __init__(
         self,
         added: list[ StationChange ],
         ended: list[ StationChange ],
         extended: list[ StationChange ] ) -> None:
      self.added = added
      self.ended = ended
      self.extended = extended


   def count( self ) -> int:
      return len( self.added ) + len( self.ended ) + len( self.extended )


   @classmethod
   def horizon( cls, today: date ) -> date:
      return CalendarDates.two_weeks_later( today )


   @classmethod
   def kept_end( cls, end: date | None, today: date ) -> date | None:
      horizon = cls.horizon( today )

      if end == None or end >= horizon:
         return end

      return horizon


   @classmethod
   def as_date( cls, value: str | date | None ) -> date | None:
      if value in ( None, '' ):
         return None

      return DateValues.parse_date_value( value )


   @classmethod
   def closure_row(
         cls,
         record: TransportationStationStatusRecord,
         today: date ) -> StationChange | None:
      if not record.is_closed:
         return None

      if not DateValues.is_date_in_range( today, record.closed_start, record.closed_end ):
         return None

      start = cls.as_date( record.closed_start )

      if start == None:
         return None

      end = cls.as_date( record.closed_end )

      return StationChange(
         record.station,
         record.closed_message or '',
         start,
         end,
      )


   @classmethod
   def active(
         cls,
         records: list[ TransportationStationStatusRecord ],
         today: date ) -> list[ StationChange ]:
      rows = []

      for record in records:
         closure = cls.closure_row( record, today )

         if closure == None:
            continue

         rows.append( closure )

      return rows


   @classmethod
   def same( cls, notice: StationClosure, item: StationChange ) -> bool:
      return item.station == notice.station and item.message == notice.message


   @classmethod
   def matched(
         cls,
         notice: StationClosure,
         stored: list[ StationChange ] ) -> StationChange | None:
      for item in stored:
         if cls.same( notice, item ):
            return item

      return None


   @classmethod
   def on_website( cls, item: StationChange, notices: list[ StationClosure ] ) -> bool:
      return any( cls.same( notice, item ) for notice in notices )


   @classmethod
   def notice_for(
         cls,
         item: StationChange,
         notices: list[ StationClosure ] ) -> StationClosure | None:
      for notice in notices:
         if cls.same( notice, item ):
            return notice

      return None


   @classmethod
   def addition( cls, notice: StationClosure, today: date ) -> StationChange:
      if notice.dated():
         return StationChange( notice.station, notice.message, notice.start, notice.end )

      return StationChange(
         notice.station,
         notice.message,
         today,
         cls.horizon( today ),
      )


   @classmethod
   def added(
         cls,
         notices: list[ StationClosure ],
         stored: list[ StationChange ],
         today: date ) -> list[ StationChange ]:
      return [
         cls.addition( notice, today )
         for notice in notices
         if cls.matched( notice, stored ) == None
      ]


   @classmethod
   def ended(
         cls,
         notices: list[ StationClosure ],
         stored: list[ StationChange ] ) -> list[ StationChange ]:
      return [
         item
         for item in stored
         if not cls.on_website( item, notices )
      ]


   @classmethod
   def extension(
         cls,
         item: StationChange,
         notices: list[ StationClosure ],
         today: date ) -> StationChange | None:
      notice = cls.notice_for( item, notices )

      if notice == None:
         return None

      if notice.dated():
         start = notice.start
         end = notice.end
      else:
         start = item.start
         end = cls.kept_end( item.end, today )

      if start == item.start and end == item.end:
         return None

      return StationChange( item.station, item.message, start, end )


   @classmethod
   def extended(
         cls,
         notices: list[ StationClosure ],
         stored: list[ StationChange ],
         today: date ) -> list[ StationChange ]:
      return [
         change
         for change in ( cls.extension( item, notices, today ) for item in stored )
         if change != None
      ]


   @classmethod
   def build(
         cls,
         notices: list[ StationClosure ],
         records: list[ TransportationStationStatusRecord ],
         today: date ) -> StationClosurePlan:
      stored = cls.active( records, today )
      return cls(
         cls.added( notices, stored, today ),
         cls.ended( notices, stored ),
         cls.extended( notices, stored, today ),
      )
