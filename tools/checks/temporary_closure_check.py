from __future__ import annotations

from datetime import date

from .check_report import CheckReport
from .temporary_closure_change import TemporaryClosureChange
from .temporary_closure_plan import TemporaryClosurePlan


class TemporaryClosureCheck():
   @classmethod
   def ordered(
         cls,
         changes: list[ TemporaryClosureChange ] ) -> list[ TemporaryClosureChange ]:
      return sorted( changes, key=lambda change: change.place.casefold() )


   @classmethod
   def remaining( cls, lines: list[ str ] ) -> int:
      phrases = (
         CheckReport.text( 'checks.setTemporaryClosureFrom' ),
         CheckReport.text( 'checks.openedTemporaryClosure' ),
         CheckReport.text( 'checks.extendedTemporaryClosureThrough' ),
      )

      return sum(
         all( phrase not in line for phrase in phrases )
         for line in lines
      )


   @classmethod
   def run(
         cls,
         report: str,
         plan: TemporaryClosurePlan,
         today: date ) -> int:
      added = [ change.added_line() for change in cls.ordered( plan.added ) ]
      ended = [ change.ended_line() for change in cls.ordered( plan.ended ) ]
      extended = [ change.extended_line() for change in cls.ordered( plan.extended ) ]
      print( CheckReport.heading( report, today ) )
      print()
      CheckReport.print_category( 'checks.websiteOnly', added )
      CheckReport.print_category( 'checks.appOnly', ended )
      CheckReport.print_category( 'checks.windowsDoNotAlign', extended )
      return cls.remaining( added + ended + extended )
