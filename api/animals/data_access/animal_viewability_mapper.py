from __future__ import annotations

from .animal_viewability_record import AnimalViewabilityRecord
from ...shared.enums import AnimalViewingScope
from ...shared.value_conversion import ValueConversion
from ...types import Row


def map_animal_viewability_row( row: Row ) -> AnimalViewabilityRecord:
   return AnimalViewabilityRecord(
      species=row[ 'SPECIES' ],
      latin_name=row[ 'LATIN_NAME' ],
      min_temperature=row[ 'MIN_TEMPERATURE' ],
      general_viewing_tips=row[ 'GENERAL_VIEWING_TIPS' ],
      seasonal_viewing_tips=row[ 'SEASONAL_VIEWING_TIPS' ],
      identification=row[ 'IDENTIFICATION' ],
      habitat_and_range=row[ 'HABITAT_AND_RANGE' ],
      diet_and_feeding=row[ 'DIET_AND_FEEDING' ],
      behaviour_and_social_life=row[ 'BEHAVIOUR_AND_SOCIAL_LIFE' ],
      adaptations=row[ 'ADAPTATIONS' ],
      reproduction_and_life_cycle=row[ 'REPRODUCTION_AND_LIFE_CYCLE' ],
      animals_at_the_zoo=row[ 'ANIMALS_AT_THE_ZOO' ],
      exhibit=row[ 'EXHIBIT' ],
      seasonal_viewing_summary=row[ 'SEASONAL_VIEWING_SUMMARY' ],
      seasonal_viewing_information=row[ 'SEASONAL_VIEWING_INFORMATION' ],
      include_all_viewing_spots=ValueConversion.as_nullable_boolean(
         row[ 'INCLUDE_ALL_VIEWING_SPOTS' ] ),
      enclosure_type=row[ 'ENCLOSURE_TYPE' ],
      enclosure_name=row[ 'ENCLOSURE_NAME' ],
      seasonally_off_display_message=row[ 'SEASONALLY_OFF_DISPLAY_MESSAGE' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ],
      is_off_display=row[ 'IS_OFF_DISPLAY' ],
      viewing_scope=AnimalViewingScope.normalize( row[ 'VIEWING_SCOPE' ] ),
      off_display_message=row[ 'OFF_DISPLAY_MESSAGE' ],
      off_display_start=row[ 'OFF_DISPLAY_START' ],
      off_display_end=row[ 'OFF_DISPLAY_END' ],
      schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
      schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
      daily_start_time=row[ 'DAILY_START_TIME' ],
      daily_end_time=row[ 'DAILY_END_TIME' ],
      viewing_message=row[ 'VIEWING_MESSAGE' ],
      alert_message=row[ 'ALERT_MESSAGE' ],
      alert_start_date=row[ 'ALERT_START_DATE' ],
      alert_end_date=row[ 'ALERT_END_DATE' ],
      is_closed=row[ 'IS_CLOSED' ],
      closed_message=row[ 'CLOSED_MESSAGE' ],
      closed_start=row[ 'CLOSED_START' ],
      closed_end=row[ 'CLOSED_END' ],
      animal_day_seasonal_multiplier=row[ 'ANIMAL_DAY_SEASONAL_MULTIPLIER' ],
      exhibit_day_seasonal_availability_multiplier=row[ 'EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER' ] )


def map_animal_viewability_rows( rows: list[ Row ] ) -> list[ AnimalViewabilityRecord ]:
   return [
      map_animal_viewability_row( row )
      for row in rows
   ]
