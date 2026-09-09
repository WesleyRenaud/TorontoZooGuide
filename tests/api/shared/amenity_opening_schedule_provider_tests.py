from __future__ import annotations

from api.restaurants.data_access.restaurant_schedule_mapper import RestaurantScheduleMapper
from api.shared.amenity_opening_schedule_provider import AmenityOpeningScheduleProvider
from api.shared.enums.amenity_name_field import AmenityNameField


def Test_AmenityOpeningScheduleProvider_TestRestaurantConfig_ExpectOwnerColumnAndTables() -> None:
   provider = AmenityOpeningScheduleProvider(
      name_field=AmenityNameField.RESTAURANT,
      opening_table='RestaurantOpeningSchedule',
      override_table='RestaurantScheduleOverride',
      map_records=RestaurantScheduleMapper.map_records,
   )

   assert provider.owner_column == 'RESTAURANT'
   assert provider.opening_table == 'RestaurantOpeningSchedule'
   assert provider.override_table == 'RestaurantScheduleOverride'
   assert provider.name_field is AmenityNameField.RESTAURANT
