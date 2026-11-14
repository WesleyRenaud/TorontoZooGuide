from __future__ import annotations

import re

from api.app_string_provider import AppStringProvider
from api.shared.text_values import TextValues


class ViewingAlertSentence():
   SENTENCE_RE = re.compile( r'(?<=[.!?])\s+' )
   VERB_RE = re.compile( r'\b(?:is|are|was|were)\b', re.I )
   WHERE_RE = re.compile( r'\b(?:see|seen|viewable|pool|outdoor|outdoors)\b', re.I )
   CLOSED_RE = re.compile( r'\b(?:close|closed|closing|closure)\b', re.I )
   WORD_RE = re.compile( r"[A-Za-z][A-Za-z'-]*" )
   SMALL_WORDS = { 'a', 'an', 'the', 'for', 'of', 'and', 'to', 'in', 'on' }


   @classmethod
   def sentences( cls, text: str ) -> str:
      parts = [
         part
         for part in cls.SENTENCE_RE.split( ' '.join( text.split() ) )
         if part != ''
      ]
      return ' '.join( parts[ :2 ] )


   @classmethod
   def clause( cls, text: str ) -> str:
      cleaned = ' '.join( text.split() ).strip( ' "' )

      if cleaned == '':
         return ''

      if cleaned[ -1 ] not in '.!?':
         return f'{ cleaned }.'

      return cleaned


   @classmethod
   def notice_parts( cls, text: str ) -> list[ str ]:
      return [
         part
         for part in ( cls.clause( piece ) for piece in cls.SENTENCE_RE.split( text ) )
         if part != ''
      ]


   @classmethod
   def headline( cls, text: str ) -> bool:
      words = [
         word
         for word in cls.WORD_RE.findall( text )
         if word.casefold() not in cls.SMALL_WORDS
      ]

      if len( words ) < 3:
         return False

      capped = [ word for word in words if word[ 0 ].isupper() ]
      return len( capped ) / len( words ) >= 0.6


   @classmethod
   def sentence_case( cls, text: str ) -> str:
      lowered = text.casefold().lstrip()

      if lowered == '':
         return ''

      return lowered[ 0 ].upper() + lowered[ 1: ]


   @classmethod
   def sentence_from_title( cls, title: str ) -> str:
      text = cls.clause( title )

      if text == '' or cls.VERB_RE.search( text ) == None:
         return ''

      if cls.headline( text ):
         return cls.clause( cls.sentence_case( text ) )

      return text


   @classmethod
   def source_sentences( cls, title: str, description: str ) -> list[ str ]:
      parts = []
      titled = cls.sentence_from_title( title )

      if titled != '':
         parts.append( titled )

      parts.extend( cls.notice_parts( description ) )
      return parts


   @classmethod
   def closure_sentence( cls, parts: list[ str ] ) -> str:
      for part in parts:
         if cls.CLOSED_RE.search( part ) != None:
            return part

      return ''


   @classmethod
   def where_sentence( cls, parts: list[ str ] ) -> str:
      for part in parts:
         if cls.WHERE_RE.search( part ) != None and cls.CLOSED_RE.search( part ) == None:
            return part

      return ''


   @classmethod
   def with_exhibit( cls, sentence: str, exhibit: str ) -> str:
      if sentence == '' or exhibit.casefold() in sentence.casefold():
         return sentence

      marker = AppStringProvider.format( 'guestStatus.animals.isClosed' )
      index = sentence.casefold().find( marker )

      if index >= 0:
         return AppStringProvider.format(
            'guestStatus.animals.beforeClosed',
            before=sentence[ :index ],
            exhibit=exhibit,
            after=sentence[ index: ],
         )

      body = sentence[ :-1 ] if sentence.endswith( '.' ) else sentence
      return AppStringProvider.format(
         'guestStatus.animals.sentenceAtExhibit',
         sentence=body,
         exhibit=exhibit,
      )


   @classmethod
   def as_written( cls, species: str, text: str ) -> str:
      found = re.search( re.escape( species ), text, re.I )

      if found == None:
         return species

      return found.group( 0 )


   @classmethod
   def plural( cls, name: str ) -> str:
      if name.casefold().endswith( 's' ):
         return name

      return TextValues.plural( name )


   @classmethod
   def former_home( cls, species: str, text: str ) -> bool:
      key = species.casefold()
      folded = text.casefold()
      singular = AppStringProvider.format( 'guestStatus.animals.formerSpecies', species=key )
      plural = AppStringProvider.format(
         'guestStatus.animals.formerSpecies',
         species=TextValues.plural( key ),
      )
      return singular in folded or plural in folded


   @classmethod
   def seen( cls, species: str, text: str, place: str ) -> str:
      return AppStringProvider.format(
         'guestStatus.animals.canBeSeen',
         species=cls.plural( cls.as_written( species, text ) ),
         place=place,
      )


   @classmethod
   def follow( cls, first: str, second: str ) -> str:
      if first == '':
         return second

      if second == '':
         return first

      return cls.sentences( TextValues.beside( first, second ) )


   @classmethod
   def former_habitat( cls, species: str, exhibit: str, notice: str ) -> str:
      building = AppStringProvider.format( 'guestStatus.animals.underConstruction' )
      status = (
         building
         if building in notice.casefold()
         else AppStringProvider.format( 'guestStatus.animals.habitatClosed' )
      )
      seen = cls.seen(
         species,
         notice,
         AppStringProvider.format( 'guestStatus.animals.atLocation', exhibit=exhibit ),
      )
      habitat = AppStringProvider.format(
         'guestStatus.animals.formerHabitat',
         species=cls.as_written( species, notice ),
         status=status,
      )
      return cls.follow( seen, habitat )


   @classmethod
   def off_display_at( cls, species: str, exhibit: str, notice: str ) -> str:
      return AppStringProvider.format(
         'guestStatus.animals.offDisplayAtExhibit',
         species=cls.as_written( species, notice ),
         exhibit=exhibit,
      )


   @classmethod
   def on_display( cls, parts: list[ str ], closed: str, exhibit: str ) -> str:
      where = cls.where_sentence( parts )

      if closed == '':
         where = cls.with_exhibit( where, exhibit )

      return cls.follow( closed, where )


   @classmethod
   def write(
         cls,
         species: str,
         exhibit: str,
         off_display: bool,
         scope: str,
         title: str,
         description: str ) -> str:
      parts = cls.source_sentences( title, description )
      closed = cls.with_exhibit( cls.closure_sentence( parts ), exhibit )
      notice = TextValues.beside( title, description )
      limited = scope.casefold()

      if cls.former_home( species, notice ):
         return cls.former_habitat( species, exhibit, notice )

      if off_display and limited == 'indoor':
         outside = AppStringProvider.format( 'guestStatus.animals.outside' )
         return cls.follow( closed, cls.seen( species, notice, outside ) )

      if off_display and limited == 'outdoor':
         inside = AppStringProvider.format( 'guestStatus.animals.inside' )
         return cls.follow( closed, cls.seen( species, notice, inside ) )

      if off_display:
         return cls.follow( cls.off_display_at( species, exhibit, notice ), closed )

      return cls.on_display( parts, closed, exhibit )
