from __future__ import annotations


def wire_schedule_row(
      time: str,
      *,
      monday: bool = True,
      tuesday: bool = False,
      wednesday: bool = False,
      thursday: bool = False,
      friday: bool = False,
      saturday: bool = False,
      sunday: bool = False ) -> dict[ str, object ]:
   return {
      'time': time,
      'monday': monday,
      'tuesday': tuesday,
      'wednesday': wednesday,
      'thursday': thursday,
      'friday': friday,
      'saturday': saturday,
      'sunday': sunday,
   }


def wire_schedule_rows(
      *times: str,
      monday: bool = True,
      tuesday: bool = False,
      wednesday: bool = False,
      thursday: bool = False,
      friday: bool = False,
      saturday: bool = False,
      sunday: bool = False ) -> list[ dict[ str, object ] ]:
   return [
      wire_schedule_row(
         time,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday )
      for time in times
   ]
