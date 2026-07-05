from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import AnimalViewingScope
from ...types import Coordinate, DateKey, ScheduleTimeKey, SeasonalMultiplier


@dataclass( frozen=True )
class AnimalViewabilityRecord:
   species: str
   latin_name: str | None
   min_temperature: float | None
   general_viewing_tips: str | None
   seasonal_viewing_tips: str | None
   identification: str | None
   habitat_and_range: str | None
   diet_and_feeding: str | None
   behaviour_and_social_life: str | None
   adaptations: str | None
   reproduction_and_life_cycle: str | None
   animals_at_the_zoo: str | None
   exhibit: str
   seasonal_viewing_summary: str | None
   seasonal_viewing_information: str | None
   enclosure_type: str | None
   enclosure_name: str | None
   seasonally_off_display_message: str | None
   x_coord: Coordinate
   y_coord: Coordinate
   is_off_display: bool | None
   viewing_scope: AnimalViewingScope | None
   off_display_message: str | None
   off_display_start: DateKey | None
   off_display_end: DateKey | None
   schedule_start_date: DateKey | None
   schedule_end_date: DateKey | None
   daily_start_time: ScheduleTimeKey
   daily_end_time: ScheduleTimeKey
   viewing_message: str | None
   alert_message: str | None
   alert_start_date: DateKey | None
   alert_end_date: DateKey | None
   is_closed: bool | None
   closed_message: str | None
   closed_start: DateKey | None
   closed_end: DateKey | None
   animal_day_seasonal_multiplier: SeasonalMultiplier
   exhibit_day_seasonal_availability_multiplier: SeasonalMultiplier
   include_all_viewing_spots: bool | None = None
