from __future__ import annotations

from api.restaurants.data_access.restaurant_schedule_mapper import RestaurantScheduleMapper
from api.shared.amenity_opening_schedule_provider import AmenityOpeningScheduleProvider
from api.shared.enums.amenity_name_field import AmenityNameField


def Test_AmenityOpeningScheduleProvider_TestRestaurantConfig_ExpectOwnerColumnAndTables() -> None:
   name_field = AmenityNameField.RESTAURANT
   opening_table = 'RestaurantOpeningSchedule'
   override_table = 'RestaurantScheduleOverride'
   provider = AmenityOpeningScheduleProvider(
      name_field=name_field,
      opening_table=opening_table,
      override_table=override_table,
      map_records=RestaurantScheduleMapper.map_records )

   assert provider.owner_column == name_field.value.upper()
   assert provider.opening_table == opening_table
   assert provider.override_table == override_table
   assert provider.name_field is name_field
