from ...shared.console_date_range import resolve_open_ended_console_date_range
from ...shared.strings import SharedStrings
from .exhibit_closed_status import ExhibitClosedStatus


def build_exhibit_closed_status(
      exhibit,
      start_date,
      end_date,
      message ):
   date_range = resolve_open_ended_console_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Exhibits.temporarily_closed( exhibit )

   return ExhibitClosedStatus(
      exhibit=exhibit,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
