from __future__ import annotations

from .category import Category
from .count import Count
from .detail_item import DetailItem
from .section import Section


class ReportDraft():
   def __init__( self ) -> None:
      self.sections: list[ Section ] = []
      self.counts: list[ Count ] = []
      self.fixed_count = 0
      self.current: Section | None = None
      self.category: Category | None = None
      self.item: DetailItem | None = None


   def finish_category( self ) -> None:
      if self.current is not None and self.category is not None:
         self.current.categories.append( self.category )

      self.category = None
      self.item = None


   def finish_section( self ) -> None:
      self.finish_category()

      if self.current is not None:
         self.sections.append( self.current )

      self.current = None


   def start_section( self, kind: str, day: str, note: str ) -> None:
      self.finish_section()
      self.current = Section( kind, day, note, [] )


   def start_category( self, title: str, count: int ) -> None:
      self.finish_category()
      self.category = Category( title, count, [] )


   def add_note( self, text: str ) -> None:
      if self.current.note == '':
         self.current.note = text
         return

      self.current.note = f'{ self.current.note } { text }'


   def add_detail( self, text: str ) -> None:
      if self.item is None:
         self.add_item( text )
         return

      self.item.details.append( text )


   def add_item( self, text: str ) -> None:
      self.item = DetailItem( text, [] )
      self.category.items.append( self.item )
