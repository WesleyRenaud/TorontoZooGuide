from __future__ import annotations

import re

from api.shared.text_values import TextValues
from .restroom_notice import RestroomNotice
from .viewing_alert_sentence_builder import ViewingAlertSentenceBuilder
from .website_closure import WebsiteClosure


class RestroomNoticeReader():
   PLACES = (
      ( 'Canadian Domain Zoomobile Stop Restroom', ( 'canadian domain zoomobile', ) ),
      ( 'African Rainforest Restroom', ( 'african rainforest', ) ),
      ( 'Africa Restaurant Restroom', ( 'africa restaurant', ) ),
      ( 'Caribou Café Restroom', ( 'caribou café', 'caribou cafe' ) ),
      ( 'Simba Safari Lodge Restroom', ( 'simba safari', ) ),
      ( 'Splash Island Restroom', ( 'splash island', ) ),
      ( 'Zootique Restroom', ( 'zootique', ) ),
      ( 'Entrance Restroom', ( 'front entrance', ) ),
      ( 'Eurasia Restroom', ( 'eurasia', ) ),
      ( 'Canadian Domain Restroom', ( 'canadian domain', ) ),
   )
   WASHROOM_RE = re.compile( r'\b(?:washrooms?|restrooms?|bathrooms?)\b', re.I )
   SKIP_RE = re.compile( r'\b(?:nearest|alternate)\b|remain open', re.I )
   OPEN_LATE_RE = re.compile( r'open late', re.I )
   WEEKDAY_RE = re.compile( r'\bweekdays\b|monday to friday', re.I )
   CLOSED_RE = re.compile( r'\b(?:close|closed|closing|closure|unavailable)\b', re.I )


   @classmethod
   def text( cls, notice: WebsiteClosure ) -> str:
      title = notice.title.strip()

      if title != '' and title[ -1 ] not in '.!?':
         title = f'{ title }.'

      return TextValues.beside( title, notice.description )


   @classmethod
   def kind( cls, sentence: str ) -> str | None:
      folded = sentence.casefold()

      if cls.SKIP_RE.search( folded ) != None:
         return None

      if cls.WASHROOM_RE.search( folded ) == None:
         return None

      if cls.OPEN_LATE_RE.search( folded ) != None:
         return 'alert'

      if cls.CLOSED_RE.search( folded ) == None:
         return None

      if cls.WEEKDAY_RE.search( folded ) != None:
         return 'alert'

      return 'closure'


   @classmethod
   def places( cls, sentence: str ) -> list[ str ]:
      folded = sentence.casefold()
      found = []

      for title, phrases in cls.PLACES:
         phrase = ''

         for candidate in phrases:
            if candidate in folded:
               phrase = candidate
               break

         if phrase == '':
            continue

         found.append( title )
         folded = folded.replace( phrase, ' ', 1 )

      return found


   @classmethod
   def read( cls, page_html: str ) -> list[ RestroomNotice ]:
      found = {}

      for notice in WebsiteClosure.notices( page_html ):
         for sentence in ViewingAlertSentenceBuilder.notice_parts( cls.text( notice ) ):
            kind = cls.kind( sentence )

            if kind == None:
               continue

            for restroom in cls.places( sentence ):
               key = ( restroom, kind )

               if key in found:
                  continue

               found[ key ] = RestroomNotice( restroom, sentence, kind == 'closure' )

      return list( found.values() )
