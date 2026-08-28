from __future__ import annotations

from datetime import date

from api.animals.data_access.animal_viewability_record import AnimalViewabilityRecord
from api.animals.domain.itinerary_animal_records_filter_builder import ItineraryAnimalRecordsFilterBuilder


ANIMAL_SPECIES = 'Asian Wild Horse'
ANIMAL_EXHIBIT = 'Eurasia Wilds'
WALKABLE_ENCLOSURE_NAME = 'Shady Acres'
ZOOMOBILE_ONLY_ENCLOSURE_NAME = 'Eurasia Drive Thru'
ENCLOSURE_TYPE = 'Outdoor'


def _make_animal_viewability_record(
      *,
      enclosure_name: str,
      is_zoomobile_only: bool ) -> AnimalViewabilityRecord:
   return AnimalViewabilityRecord(
      species=ANIMAL_SPECIES,
      latin_name=None,
      min_temperature=None,
      general_viewing_tips=None,
      seasonal_viewing_tips=None,
      identification=None,
      habitat_and_range=None,
      diet_and_feeding=None,
      behaviour_and_social_life=None,
      adaptations=None,
      reproduction_and_life_cycle=None,
      animals_at_the_zoo=None,
      exhibit=ANIMAL_EXHIBIT,
      seasonal_viewing_summary=None,
      seasonal_viewing_information=None,
      enclosure_type=ENCLOSURE_TYPE,
      enclosure_name=enclosure_name,
      seasonally_off_display_message=None,
      x_coord=1.0,
      y_coord=1.0,
      is_off_display=None,
      viewing_scope=None,
      off_display_message=None,
      off_display_start=None,
      off_display_end=None,
      schedule_start_date=None,
      schedule_end_date=None,
      daily_start_time=None,
      daily_end_time=None,
      viewing_message=None,
      alert_message=None,
      alert_start_date=None,
      alert_end_date=None,
      is_closed=None,
      closed_message=None,
      closed_start=None,
      closed_end=None,
      animal_day_seasonal_multiplier=1.0,
      exhibit_day_seasonal_availability_multiplier=1.0,
      include_all_viewing_spots=None,
      is_zoomobile_only=is_zoomobile_only )


def Test_Filter_TestZoomobileOnlyRecords_ExpectWalkableEnclosureOnly() -> None:
   records = [
      _make_animal_viewability_record(
         enclosure_name=WALKABLE_ENCLOSURE_NAME,
         is_zoomobile_only=False ),
      _make_animal_viewability_record(
         enclosure_name=ZOOMOBILE_ONLY_ENCLOSURE_NAME,
         is_zoomobile_only=True ),
   ]

   filtered = ItineraryAnimalRecordsFilterBuilder.filter( records )

   assert [
      ( record.species, record.enclosure_name )
      for record in filtered
   ] == [
      ( ANIMAL_SPECIES, WALKABLE_ENCLOSURE_NAME ),
   ]
