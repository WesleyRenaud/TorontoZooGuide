from enum import Enum


class ExhibitStatus( str, Enum ):
   CLOSED = 'closed'
   OPEN = 'open'
   UNKNOWN = 'unknown'
