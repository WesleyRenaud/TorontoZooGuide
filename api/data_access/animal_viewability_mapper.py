from .animal_viewability_record import AnimalViewabilityRecord


def get_row_value( row, key, default=None ):
   if hasattr( row, 'keys' ) and key not in row.keys():
      return default

   return row[ key ]


def map_animal_viewability_row( row ):
   return AnimalViewabilityRecord(
      species=get_row_value( row, 'SPECIES' ),
      latin_name=get_row_value( row, 'LATIN_NAME' ),
      min_temperature=get_row_value( row, 'MIN_TEMPERATURE' ),
      general_viewing_tips=get_row_value( row, 'GENERAL_VIEWING_TIPS' ),
      seasonal_viewing_tips=get_row_value( row, 'SEASONAL_VIEWING_TIPS' ),
      identification=get_row_value( row, 'IDENTIFICATION' ),
      habitat_and_range=get_row_value( row, 'HABITAT_AND_RANGE' ),
      diet_and_feeding=get_row_value( row, 'DIET_AND_FEEDING' ),
      behaviour_and_social_life=get_row_value( row, 'BEHAVIOUR_AND_SOCIAL_LIFE' ),
      adaptations=get_row_value( row, 'ADAPTATIONS' ),
      reproduction_and_life_cycle=get_row_value( row, 'REPRODUCTION_AND_LIFE_CYCLE' ),
      animals_at_the_zoo=get_row_value( row, 'ANIMALS_AT_THE_ZOO' ),
      exhibit=get_row_value( row, 'EXHIBIT' ),
      seasonal_viewing_summary=get_row_value( row, 'SEASONAL_VIEWING_SUMMARY' ),
      seasonal_viewing_information=get_row_value( row, 'SEASONAL_VIEWING_INFORMATION' ),
      enclosure_type=get_row_value( row, 'ENCLOSURE_TYPE' ),
      seasonally_off_display_message=get_row_value( row, 'SEASONALLY_OFF_DISPLAY_MESSAGE' ),
      x_coord=get_row_value( row, 'X_COORD' ),
      y_coord=get_row_value( row, 'Y_COORD' ),
      is_off_display=get_row_value( row, 'IS_OFF_DISPLAY' ),
      off_display_message=get_row_value( row, 'OFF_DISPLAY_MESSAGE' ),
      off_display_start=get_row_value( row, 'OFF_DISPLAY_START' ),
      off_display_end=get_row_value( row, 'OFF_DISPLAY_END' ),
      schedule_start_date=get_row_value( row, 'SCHEDULE_START_DATE' ),
      schedule_end_date=get_row_value( row, 'SCHEDULE_END_DATE' ),
      daily_start_time=get_row_value( row, 'DAILY_START_TIME' ),
      daily_end_time=get_row_value( row, 'DAILY_END_TIME' ),
      viewing_message=get_row_value( row, 'VIEWING_MESSAGE' ),
      alert_message=get_row_value( row, 'ALERT_MESSAGE' ),
      alert_start_date=get_row_value( row, 'ALERT_START_DATE' ),
      alert_end_date=get_row_value( row, 'ALERT_END_DATE' ),
      is_closed=get_row_value( row, 'IS_CLOSED' ),
      closed_message=get_row_value( row, 'CLOSED_MESSAGE' ),
      closed_start=get_row_value( row, 'CLOSED_START' ),
      closed_end=get_row_value( row, 'CLOSED_END' ),
      animal_day_seasonal_multiplier=get_row_value( row, 'ANIMAL_DAY_SEASONAL_MULTIPLIER' ),
      exhibit_day_seasonal_availability_multiplier=get_row_value( row, 'EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER' ) )


def map_animal_viewability_rows( rows ):
   return [
      map_animal_viewability_row( row )
      for row in rows
   ]
