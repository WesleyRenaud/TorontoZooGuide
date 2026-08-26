from __future__ import annotations

from .event_mapper import EventMapper
from ...models import Event
from ...types import Connection, DateKey


class EventProvider():
   @classmethod
   def insert_event( cls, conn: Connection, event: Event ) -> bool:
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
         conn: Connection,
         as_of_date: DateKey ) -> list[ Event ]:
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
