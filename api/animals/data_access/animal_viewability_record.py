from dataclasses import dataclass


@dataclass( frozen=True )
class AnimalViewabilityRecord:
   species: object
   latin_name: object
   min_temperature: object
   general_viewing_tips: object
   seasonal_viewing_tips: object
   identification: object
   habitat_and_range: object
   diet_and_feeding: object
   behaviour_and_social_life: object
   adaptations: object
   reproduction_and_life_cycle: object
   animals_at_the_zoo: object
   exhibit: object
   seasonal_viewing_summary: object
   seasonal_viewing_information: object
   enclosure_type: object
   seasonally_off_display_message: object
   x_coord: object
   y_coord: object
   is_off_display: object
   off_display_message: object
   off_display_start: object
   off_display_end: object
   schedule_start_date: object
   schedule_end_date: object
   daily_start_time: object
   daily_end_time: object
   viewing_message: object
   alert_message: object
   alert_start_date: object
   alert_end_date: object
   is_closed: object
   closed_message: object
   closed_start: object
   closed_end: object
   animal_day_seasonal_multiplier: object
   exhibit_day_seasonal_availability_multiplier: object
