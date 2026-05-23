from __future__ import annotations

from .animal_viewing_alert import AnimalViewingAlert
from ...shared.date_values import DateValues
from ...shared.strings import SharedStrings
from ...types import DateInput


def build_animal_viewing_alert(
      species: str,
      exhibit: str,
      alert_start_date: DateInput,
      alert_end_date: DateInput,
      message: str ) -> AnimalViewingAlert:
   date_range = DateValues.resolve_open_ended_date_range(
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
