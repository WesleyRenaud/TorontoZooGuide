from __future__ import annotations

from .event_mapper import EventMapper
from ...models import Event
from ...types import Types


class EventProvider():
   @classmethod
   def insert_event( cls, conn: Types.Connection, event: Event ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO ZooEvent (
                     NAME,
                     LOCATION,
                     DESCRIPTION,
                     LINK,
                     START_DATE,
                     END_DATE
                  )
                  VALUES (?, ?, ?, ?, ?, ?)
                  ON CONFLICT(NAME, START_DATE) DO NOTHING;
            """,
            (
               event.name,
               event.location,
               event.description,
               event.link,
               event.start_date,
               event.end_date,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def fetch_events(
         cls,
         conn: Types.Connection,
         as_of_date: Types.DateKey ) -> list[ Event ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     NAME,
                     LOCATION,
                     DESCRIPTION,
                     LINK,
                     START_DATE,
                     END_DATE
                  FROM ZooEvent
                  WHERE END_DATE IS NULL
                     OR END_DATE = ''
                     OR END_DATE >= ?
                  ORDER BY START_DATE ASC, NAME ASC;
            """,
            ( as_of_date, ) )

         return EventMapper.map_records( data.fetchall() )

      finally:
         cur.close()
