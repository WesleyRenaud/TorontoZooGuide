from __future__ import annotations

# Temporary exhibit ordering for primitive bulk animal scheduling.
BULK_SCHEDULE_EXHIBIT_ORDER: tuple[ str, ... ] = (
   'Indo-Malaya Outdoor',
   'Malayan Woods Pavilion',
   'Indo-Malaya Pavilion',
   'African Rainforest Pavilion',
   'Africa Savanna',
   'Canadian Domain',
   'Americas Pavilion',
   'Mayan Temple',
   'Tundra Trek',
   'Australasia Pavilion',
   'Australasia Outdoor',
   'Eurasia Wilds',
   'Goat World',
   'Kids Zoo',
)

_BULK_SCHEDULE_EXHIBIT_RANK = {
   exhibit_name: rank
   for rank, exhibit_name in enumerate( BULK_SCHEDULE_EXHIBIT_ORDER )
}


def bulk_schedule_exhibit_rank( exhibit_name: str ) -> int:
   return _BULK_SCHEDULE_EXHIBIT_RANK.get(
      exhibit_name,
      len( BULK_SCHEDULE_EXHIBIT_ORDER ) )
