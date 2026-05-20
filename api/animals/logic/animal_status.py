from ...shared.console_date_range import resolve_open_ended_console_date_range
from ...shared.strings import SharedStrings
from .animal_off_display_status import AnimalOffDisplayStatus


def build_animal_off_display_status(
      species,
      exhibit,
      start_date,
      end_date,
   message ):
   if not message:
      message = SharedStrings.Animals.temporarily_off_display( species )

   date_range = resolve_open_ended_console_date_range(
      start_date=start_date,
      end_date=end_date )

   return AnimalOffDisplayStatus(
      species=species,
      exhibit=exhibit,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
