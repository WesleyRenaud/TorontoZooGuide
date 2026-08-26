from __future__ import annotations

from .animal_viewing_alert import AnimalViewingAlert
from ...app_strings import format_app_string
from ...shared.calendar_dates import DateValues
from ...types import DateInput


class AnimalViewingAlertBuilder():
   @classmethod
   def build(
         cls,
         species: str,
         exhibit: str,
         alert_start_date: DateInput,
         alert_end_date: DateInput,
         message: str ) -> AnimalViewingAlert:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=alert_start_date,
         end_date=alert_end_date )

      if not message:
         message = format_app_string( 'guestStatus.animals.viewingAlert', species=species )

      return AnimalViewingAlert(
         species=species,
         exhibit=exhibit,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message )
