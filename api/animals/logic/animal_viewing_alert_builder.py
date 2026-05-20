from ...shared.console_date_range import resolve_open_ended_console_date_range
from ...shared.strings import SharedStrings
from .animal_viewing_alert import AnimalViewingAlert


def build_animal_viewing_alert(
      species,
      exhibit,
      alert_start_date,
      alert_end_date,
      message ):
   date_range = resolve_open_ended_console_date_range(
      start_date=alert_start_date,
      end_date=alert_end_date )

   if not message:
      message = SharedStrings.Animals.viewing_alert( species )

   return AnimalViewingAlert(
      species=species,
      exhibit=exhibit,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
