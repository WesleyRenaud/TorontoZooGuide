def save_current_zoomobile_route_schedule( conn, schedule ):
   cur = conn.cursor()

   try:
      cur.execute( 'DELETE FROM ZoomobileRouteSchedule;' )

      cur.execute(
         """   INSERT INTO ZoomobileRouteSchedule (
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  ROUTE
               )
               VALUES ( ?, ?, ? );
         """,
         (
            schedule.start_date,
            schedule.end_date,
            schedule.route,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
