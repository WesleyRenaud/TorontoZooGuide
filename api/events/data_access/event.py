from __future__ import annotations

from ...models import Event
from ...types import Connection


def insert_event( conn: Connection, event: Event ) -> bool:
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
