from __future__ import annotations

from datetime import date

from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from .temporary_closure import TemporaryClosure
from .temporary_closure_change import TemporaryClosureChange


class TemporaryClosurePlan():
   added: list[ TemporaryClosureChange ]
   ended: list[ TemporaryClosureChange ]
   extended: list[ TemporaryClosureChange ]


   def __init__(
         self,
         added: list[ TemporaryClosureChange ],
         ended: list[ TemporaryClosureChange ],
         extended: list[ TemporaryClosureChange ] ) -> None:
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
   def same( cls, notice: TemporaryClosure, item: TemporaryClosureChange ) -> bool:
      return (
         item.place == notice.place
         and item.message == notice.message
         and item.kind == notice.kind
      )


   @classmethod
   def matched(
         cls,
         notice: TemporaryClosure,
         stored: list[ TemporaryClosureChange ] ) -> TemporaryClosureChange | None:
      for item in stored:
         if cls.same( notice, item ):
            return item

      return None


   @classmethod
   def matched_closure(
         cls,
         item: TemporaryClosureChange,
         notices: list[ TemporaryClosure ] ) -> TemporaryClosure | None:
      for notice in notices:
         if cls.same( notice, item ):
            return notice

      return None


   @classmethod
   def on_website(
         cls,
         item: TemporaryClosureChange,
         notices: list[ TemporaryClosure ] ) -> bool:
      return cls.matched_closure( item, notices ) != None


   @classmethod
   def addition( cls, notice: TemporaryClosure, today: date ) -> TemporaryClosureChange:
      return TemporaryClosureChange(
         notice.place,
         notice.message,
         notice.kind,
         today if notice.start == None else notice.start,
         cls.horizon( today ) if notice.end == None else notice.end,
         notice.photo_path,
      )


   @classmethod
   def added(
         cls,
         notices: list[ TemporaryClosure ],
         stored: list[ TemporaryClosureChange ],
         today: date ) -> list[ TemporaryClosureChange ]:
      return [
         cls.addition( notice, today )
         for notice in notices
         if cls.matched( notice, stored ) == None
         and DateValues.is_date_on_or_before( today, notice.end )
      ]


   @classmethod
   def ended(
         cls,
         notices: list[ TemporaryClosure ],
         stored: list[ TemporaryClosureChange ],
         today: date ) -> list[ TemporaryClosureChange ]:
      endings = []

      for item in stored:
         if cls.on_website( item, notices ):
            continue

         endings.append( TemporaryClosureChange(
            item.place,
            item.message,
            item.kind,
            item.start if item.start != None else today,
            CalendarDates.one_day_earlier( today ),
            item.photo_path,
         ) )

      return endings


   @classmethod
   def extended(
         cls,
         notices: list[ TemporaryClosure ],
         stored: list[ TemporaryClosureChange ],
         today: date ) -> list[ TemporaryClosureChange ]:
      extensions = []

      for item in stored:
         notice = cls.matched_closure( item, notices )

         if notice == None:
            continue

         kept = cls.kept_end( item.end, today ) if notice.end == None else notice.end

         if item.start == None or kept == None or kept == item.end:
            continue

         extensions.append( TemporaryClosureChange(
            item.place,
            item.message,
            item.kind,
            item.start,
            kept,
            item.photo_path,
         ) )

      return extensions


   @classmethod
   def build(
         cls,
         notices: list[ TemporaryClosure ],
         stored: list[ TemporaryClosureChange ],
         today: date ) -> TemporaryClosurePlan:
      return cls(
         cls.added( notices, stored, today ),
         cls.ended( notices, stored, today ),
         cls.extended( notices, stored, today ),
      )
