from enum import Enum


class ScheduleStatus( str, Enum ):
   CLOSED = 'closed'
   OPEN = 'open'
   UNKNOWN = 'unknown'
