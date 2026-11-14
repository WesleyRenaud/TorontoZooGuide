from __future__ import annotations

from datetime import date

from api.restrooms.data_access.restroom_record import RestroomRecord
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from .restroom_change import RestroomChange
from .restroom_notice import RestroomNotice


class RestroomNoticePlan():
   added: list[ RestroomChange ]
   ended: list[ RestroomChange ]
   extended: list[ RestroomChange ]


   def __init__(
         self,
         added: list[ RestroomChange ],
         ended: list[ RestroomChange ],
         extended: list[ RestroomChange ] ) -> None:
      self.added = added
      self.ended = ended
      self.extended = extended


   def count( self ) -> int:
      return len( self.added ) + len( self.ended ) + len( self.extended )


   @classmethod
   def horizon( cls, today: date ) -> date:
      return CalendarDates.one_month_later( today )


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
   def closure_row( cls, record: RestroomRecord, today: date ) -> RestroomChange | None:
      if not record.is_closed:
         return None

      if not DateValues.is_date_in_range( today, record.closed_start, record.closed_end ):
         return None

      return RestroomChange(
         record.title,
         record.closed_message or '',
         True,
         cls.as_date( record.closed_start ),
         cls.as_date( record.closed_end ),
      )


   @classmethod
   def alert_row( cls, record: RestroomRecord, today: date ) -> RestroomChange | None:
      if record.alert_message in ( None, '' ):
         return None

      if not DateValues.is_date_in_range(
            today,
            record.alert_start_date,
            record.alert_end_date ):
         return None

      return RestroomChange(
         record.title,
         record.alert_message or '',
         False,
         cls.as_date( record.alert_start_date ),
         cls.as_date( record.alert_end_date ),
      )


   @classmethod
   def active( cls, records: list[ RestroomRecord ], today: date ) -> list[ RestroomChange ]:
      rows = []

      for record in records:
         closure = cls.closure_row( record, today )
         alert = cls.alert_row( record, today )

         if closure != None:
            rows.append( closure )

         if alert != None:
            rows.append( alert )

      return rows


   @classmethod
   def same( cls, notice: RestroomNotice, item: RestroomChange ) -> bool:
      return (
         item.restroom == notice.restroom
         and item.message == notice.message
         and item.closure == notice.closure
      )


   @classmethod
   def matched(
         cls,
         notice: RestroomNotice,
         stored: list[ RestroomChange ] ) -> RestroomChange | None:
      for item in stored:
         if cls.same( notice, item ):
            return item

      return None


   @classmethod
   def on_website( cls, item: RestroomChange, notices: list[ RestroomNotice ] ) -> bool:
      return any( cls.same( notice, item ) for notice in notices )


   @classmethod
   def addition( cls, notice: RestroomNotice, today: date ) -> RestroomChange:
      return RestroomChange(
         notice.restroom,
         notice.message,
         notice.closure,
         today,
         cls.horizon( today ),
      )


   @classmethod
   def added(
         cls,
         notices: list[ RestroomNotice ],
         stored: list[ RestroomChange ],
         today: date ) -> list[ RestroomChange ]:
      return [
         cls.addition( notice, today )
         for notice in notices
         if cls.matched( notice, stored ) == None
      ]


   @classmethod
   def ended(
         cls,
         notices: list[ RestroomNotice ],
         stored: list[ RestroomChange ],
         today: date ) -> list[ RestroomChange ]:
      endings = []

      for item in stored:
         if cls.on_website( item, notices ):
            continue

         start = item.start if item.start != None else today
         endings.append( RestroomChange(
            item.restroom,
            item.message,
            item.closure,
            start,
            today,
         ) )

      return endings


   @classmethod
   def extended(
         cls,
         notices: list[ RestroomNotice ],
         stored: list[ RestroomChange ],
         today: date ) -> list[ RestroomChange ]:
      extensions = []

      for item in stored:
         if not cls.on_website( item, notices ):
            continue

         kept = cls.kept_end( item.end, today )

         if item.start == None or kept == None or kept == item.end:
            continue

         extensions.append( RestroomChange(
            item.restroom,
            item.message,
            item.closure,
            item.start,
            kept,
         ) )

      return extensions


   @classmethod
   def build(
         cls,
         notices: list[ RestroomNotice ],
         records: list[ RestroomRecord ],
         today: date ) -> RestroomNoticePlan:
      stored = cls.active( records, today )
      return cls(
         cls.added( notices, stored, today ),
         cls.ended( notices, stored, today ),
         cls.extended( notices, stored, today ),
      )
