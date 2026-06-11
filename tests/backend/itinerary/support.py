from __future__ import annotations


def guardians_talk_save_entry(
      name: str,
      *,
      start_time: str | None = None,
      end_time: str | None = None ) -> dict[ str, str | None ]:
   return {
      'name': name,
      'start_time': start_time,
      'end_time': end_time,
   }


def guardians_talk_save_entries( *names: str ) -> list[ dict[ str, str | None ] ]:
   return [
      guardians_talk_save_entry( name )
      for name in names
   ]
