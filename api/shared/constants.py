from __future__ import annotations


class Constants():
   OPEN_ENDED_SQL_DATE = '9999-12-31'
   ANIMAL_VISIBILITY_CHANGE_THRESHOLD = 20
   ITINERARY_ANIMAL_MIN_LIKELIHOOD = 40
   MIN_ITINERARY_VISIT_DURATION_MINUTES = 120
   MAX_FIXED_TIME_ITEM_WAIT_MINUTES = 30
   SCHEDULE_SLOT_STEP_SECONDS = 30
   SCHEDULED_OCCURRENCE_DAYS_AHEAD = 60
   # Insert a Zoomobile ride between two anchors when the remaining walk
   # (to board + from alight) is at most this fraction of walking the whole way.
   TRANSPORTATION_WALK_SAVINGS_MAX_REMAINING_FRACTION = 0.5
   # Reject a Zoomobile transfer when ride time is more than this multiple of
   # the direct walk minutes (allows modestly longer rides; blocks full-loop hops).
   TRANSPORTATION_RIDE_MAX_WALK_DURATION_MULTIPLIER = 2
