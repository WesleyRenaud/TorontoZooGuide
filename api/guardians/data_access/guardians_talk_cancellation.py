def save_guardians_talk_cancellation( conn, cancellation ):
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO GuardiansTalkCancellation (
                  TALK_NAME,
                  LOCATION,
                  CANCELLATION_DATE,
                  TALK_TIME
               )
               VALUES (?, ?, ?, ?)
               ON CONFLICT(TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME)
               DO NOTHING;
         """,
         (
            cancellation.talk_name,
            cancellation.location,
            cancellation.cancellation_date,
            cancellation.talk_time,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
