from __future__ import annotations

import re

from .temporary_closure_reader import TemporaryClosureReader
from .website_closure import WebsiteClosure


class ExhibitClosureSentence():
   FACILITY_RE = re.compile(
      r'\b(?:paths?|pathways?|boardwalks?|washrooms?|restrooms?|bathrooms?|'
      r'habitats?|viewing|portions?|trails?|stations?|entrances?)\b',
      re.I,
   )
   VERB_RE = re.compile(
      r'\b(?:close|closed|closing|closure|unavailable)\b'
      r'|\bnot\b(?:\s+\w+){0,3}\s+accessible\b',
      re.I,
   )


   @classmethod
   def closes( cls, sentence: str ) -> bool:
      folded = sentence.casefold()

      if TemporaryClosureReader.SKIP_RE.search( folded ) != None:
         return False

      if WebsiteClosure.SEASON_RE.search( folded ) != None:
         return False

      if TemporaryClosureReader.WEEKDAY_RE.search( folded ) != None:
         return False

      return cls.VERB_RE.search( folded ) != None


   @classmethod
   def subject( cls, clause: str ) -> str:
      match = cls.VERB_RE.search( clause )

      if match == None:
         return ''

      return clause[ : match.start() ]


   @classmethod
   def closed_names( cls, sentence: str, names: list[ str ] ) -> list[ str ]:
      found = []

      for clause in sentence.split( ':' ):
         if not cls.closes( clause ):
            continue

         subject = cls.subject( clause ).replace( "'", '' ).replace( '\u2019', '' )

         if subject.strip() == '' or cls.FACILITY_RE.search( subject ) != None:
            continue

         for name in TemporaryClosureReader.mentioned( subject, names ):
            if name not in found:
               found.append( name )

      return found
