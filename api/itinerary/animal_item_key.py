from __future__ import annotations

ANIMAL_ITEM_KEY_SEPARATOR = '||'


def format_animal_schedule_item_key( species: str, exhibit: str ) -> str:
   return (
      f'{ species.strip() }'
      f'{ ANIMAL_ITEM_KEY_SEPARATOR }'
      f'{ exhibit.strip() }' )


def parse_animal_schedule_item_key( key: str ) -> tuple[ str, str ] | None:
   parts = key.split( ANIMAL_ITEM_KEY_SEPARATOR, 1 )

   if len( parts ) != 2:
      return None

   species = parts[ 0 ].strip()
   exhibit = parts[ 1 ].strip()

   if not species or not exhibit:
      return None

   return species, exhibit
