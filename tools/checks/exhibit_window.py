from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from api.exhibits.domain.exhibit_season import ExhibitSeason
from api.exhibits.domain.exhibit_season_status import ExhibitSeasonStatus
from api.shared.date_values import DateValues
from .check_report import CheckReport


@dataclass( frozen=True )
class ExhibitWindow():
   closed: bool
   start: date
   end: date


   @classmethod
   def covers( cls, status: ExhibitSeasonStatus, today: date ) -> bool:
      return DateValues.is_date_in_range( today, status.start, status.end )


   @classmethod
   def maintenance( cls, status: ExhibitSeasonStatus | None, today: date ) -> bool:
      return (
         status is not None
         and status.is_closed
         and not status.closed_for_season
         and cls.covers( status, today )
      )


   @classmethod
   def season_closed( cls, status: ExhibitSeasonStatus | None, today: date ) -> bool:
      return (
         status is not None
         and status.is_closed
         and status.closed_for_season
         and cls.covers( status, today )
      )


   @classmethod
   def kept_start( cls, status: ExhibitSeasonStatus | None, today: date ) -> date:
      if status is None or status.start is None:
         return today

      return status.start


   @classmethod
   def replacement(
         cls,
         website_closed: bool,
         status: ExhibitSeasonStatus | None,
         season: ExhibitSeason,
         today: date ) -> ExhibitWindow | None:
      if cls.maintenance( status, today ):
         return None

      target = season.end_for( website_closed, today )
      closed_now = cls.season_closed( status, today )

      if website_closed == closed_now:
         if website_closed:
            return cls.adjusted( True, status, today, target )

         return cls.open_adjustment( status, today, target )

      return cls( website_closed, today, target )


   @classmethod
   def adjusted(
         cls,
         closed: bool,
         status: ExhibitSeasonStatus | None,
         today: date,
         target: date ) -> ExhibitWindow | None:
      if status is None or status.end == target:
         return None

      return cls( closed, cls.kept_start( status, today ), target )


   @classmethod
   def open_adjustment(
         cls,
         status: ExhibitSeasonStatus | None,
         today: date,
         target: date ) -> ExhibitWindow | None:
      if (
         status is None
         or status.is_closed
         or status.start is None
         or not cls.covers( status, today )
      ):
         return None

      return cls.adjusted( False, status, today, target )


   def detail( self ) -> str:
      key = 'checks.setClosedForSeasonFrom' if self.closed else 'checks.setOpenForSeasonFrom'
      when = (
         DateValues.format_display_date_value( self.start )
         + CheckReport.text( 'checks.dateThrough' )
         + DateValues.format_display_date_value( self.end )
         + CheckReport.text( 'checks.period' )
      )

      return CheckReport.detail_item( CheckReport.text( key ) + when )
