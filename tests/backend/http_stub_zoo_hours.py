from __future__ import annotations

from api.models import ZooHours

class ZooHoursStubMixin:
   def get_zoo_hours( self, day: int, month: str, year: int ) -> ZooHours:
         self.calls.append(
            ( 'get_zoo_hours', { 'day': day, 'month': month, 'year': year } ) )

         return ZooHours(
            date='2026-06-20',
            early_admission_time='09:00',
            open_time='09:30',
            last_admission_time='18:00',
            close_time='19:00' )
