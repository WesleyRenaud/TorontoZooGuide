from __future__ import annotations

from datetime import date

from api.models import Update
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from api.updates.domain.update_type import UpdateType
from .closure_update import ClosureUpdate
from .website_closure import WebsiteClosure


class ClosureUpdatePlan():
   added: list[ ClosureUpdate ]
   ended: list[ ClosureUpdate ]
   extended: list[ ClosureUpdate ]


   def __init__(
         self,
         added: list[ ClosureUpdate ],
         ended: list[ ClosureUpdate ],
         extended: list[ ClosureUpdate ] ) -> None:
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
   def update_start( cls, update: Update ) -> date | None:
      return DateValues.parse_date_value( update.start_date )


   @classmethod
   def update_end( cls, update: Update ) -> date | None:
      if update.end_date in ( None, '' ):
         return None

      return DateValues.parse_date_value( update.end_date )


   @classmethod
   def app_closures( cls, updates: list[ Update ] ) -> list[ Update ]:
      return [
         update
         for update in updates
         if update.update_type == UpdateType.CLOSURE.value
      ]


   @classmethod
   def same( cls, notice: WebsiteClosure, update: Update ) -> bool:
      return update.title == notice.title and update.description == notice.description


   @classmethod
   def matched( cls, notice: WebsiteClosure, updates: list[ Update ] ) -> Update | None:
      for update in updates:
         if cls.same( notice, update ):
            return update

      return None


   @classmethod
   def on_website( cls, update: Update, notices: list[ WebsiteClosure ] ) -> bool:
      return any( cls.same( notice, update ) for notice in notices )


   @classmethod
   def addition(
         cls,
         notice: WebsiteClosure,
         today: date ) -> ClosureUpdate:
      return ClosureUpdate(
         notice.title,
         notice.description,
         today,
         cls.horizon( today ),
      )


   @classmethod
   def ending( cls, update: Update, today: date ) -> ClosureUpdate | None:
      start = cls.update_start( update )

      if start == None:
         return None

      return ClosureUpdate(
         update.title,
         update.description,
         start,
         today,
      )


   @classmethod
   def extension( cls, update: Update, today: date ) -> ClosureUpdate | None:
      start = cls.update_start( update )
      end = cls.update_end( update )
      kept = cls.kept_end( end, today )

      if start == None or kept == None or kept == end:
         return None

      return ClosureUpdate(
         update.title,
         update.description,
         start,
         kept,
      )


   @classmethod
   def added(
         cls,
         notices: list[ WebsiteClosure ],
         closures: list[ Update ],
         today: date ) -> list[ ClosureUpdate ]:
      return [
         cls.addition( notice, today )
         for notice in notices
         if cls.matched( notice, closures ) == None
      ]


   @classmethod
   def ended(
         cls,
         notices: list[ WebsiteClosure ],
         closures: list[ Update ],
         today: date ) -> list[ ClosureUpdate ]:
      endings = []

      for update in closures:
         if cls.on_website( update, notices ):
            continue

         ending = cls.ending( update, today )

         if ending == None:
            continue

         endings.append( ending )

      return endings


   @classmethod
   def extended(
         cls,
         notices: list[ WebsiteClosure ],
         closures: list[ Update ],
         today: date ) -> list[ ClosureUpdate ]:
      extensions = []

      for update in closures:
         if not cls.on_website( update, notices ):
            continue

         extension = cls.extension( update, today )

         if extension == None:
            continue

         extensions.append( extension )

      return extensions


   @classmethod
   def build(
         cls,
         notices: list[ WebsiteClosure ],
         updates: list[ Update ],
         today: date ) -> ClosureUpdatePlan:
      closures = cls.app_closures( updates )
      return cls(
         cls.added( notices, closures, today ),
         cls.ended( notices, closures, today ),
         cls.extended( notices, closures, today ),
      )
