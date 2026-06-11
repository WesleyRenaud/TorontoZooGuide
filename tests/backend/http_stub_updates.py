from __future__ import annotations

from typing import Any

from http_support_constants import UPDATE_TITLE

from api.models import Update

class UpdatesStubMixin:
   def get_updates_for_visit_date( self, **kwargs: Any ) -> list[ Update ]:
         self.calls.append( ( 'get_updates_for_visit_date', kwargs ) )
         return [
            Update(
               title=UPDATE_TITLE,
               description='Come meet the new calf.',
               update_type='New Arrival',
               start_date='2026-06-01',
               end_date='2026-06-30' )
         ]


   def get_unexpired_updates( self ) -> list[ Update ]:
         self.calls.append( ( 'get_unexpired_updates', {} ) )
         return [
            Update(
               title=UPDATE_TITLE,
               description='Come meet the new calf.',
               update_type='New Arrival',
               start_date='2026-06-01',
               end_date='2026-06-30' )
         ]
