from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CHEETAH_INDO_MALAYA_ITINERARY_ENTRY, guardians_talk_save_entry
from wild_encounter_schedule_support import wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from conftest import DbControllers


CARIBOU_TALK = 'Caribou'
CARIBOU_ENTRY = {
   'species': 'Caribou',
   'exhibit': 'Tundra Trek',
}
ALDABRA_OUTDOOR_ENTRY = {
   'species': 'Aldabra Tortoise',
   'exhibit': 'African Rainforest Pavilion',
   'enclosure_name': 'Outdoor',
}
ALDABRA_INDOOR_ENCLOSURE = 'Ring-Tailed Lemur Enclosure'
GORILLA_OUTDOOR_ENTRY = {
   'species': 'Western Lowland Gorilla',
   'exhibit': 'African Rainforest Pavilion',
   'enclosure_name': 'Outdoor',
}


def _set_saturday_only_caribou_talk_schedule() -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=CARIBOU_TALK,
      location='Tundra Trek',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         '15:00',
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=True,
         sunday=False ),
      message=None,
   )


def test_date_change_dropping_talk_packs_caribou_with_enclosure_duration(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_only_caribou_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ CARIBOU_ENTRY ],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry(
            CARIBOU_TALK,
            start_time='15:00',
            end_time='15:30',
         ),
      ],
      wild_encounters=[],
      confirming_fixed_time_item_long_wait=True,
   ).success
   assert ItineraryCoordinator.bulk_schedule_animals(
      confirming_fixed_time_item_long_wait=True ).success

   saturday = ItineraryCoordinator.get_itinerary()
   covered = next(
      animal
      for animal in saturday.animals
      if animal.species == 'Caribou' )
   assert covered.covered_by_talk is True
   talk_duration_seconds = (
      DateValues.time_value_in_seconds( covered.end_time )
      - DateValues.time_value_in_seconds( covered.start_time ) )
   assert talk_duration_seconds == 30 * 60

   freeze_database_today( date( 2026, 6, 21 ) )
   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-21',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ CARIBOU_ENTRY ],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry(
            CARIBOU_TALK,
            start_time='15:00',
            end_time='15:30',
         ),
      ],
      wild_encounters=[],
   )

   assert result.success
   monday = result.itinerary
   assert monday is not None
   assert all( talk.is_deleted for talk in monday.guardians_talks ) or monday.guardians_talks == []
   caribou = next(
      animal
      for animal in monday.animals
      if animal.species == 'Caribou' )
   assert caribou.covered_by_talk is False
   assert caribou.start_time is not None
   assert caribou.end_time is not None
   packed_duration_seconds = (
      DateValues.time_value_in_seconds( caribou.end_time )
      - DateValues.time_value_in_seconds( caribou.start_time ) )
   assert packed_duration_seconds == 3 * 60


def test_date_change_swaps_outdoor_aldabra_for_indoor_and_closes_schedule_hole(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 7, 19 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-07-19',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
         ALDABRA_OUTDOOR_ENTRY,
         GORILLA_OUTDOOR_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      visit_date_temp=28,
   ).success
   assert ItineraryCoordinator.bulk_schedule_animals(
      visit_date_temp=28 ).success

   warm_day = ItineraryCoordinator.get_itinerary( visit_date_temp=28 )
   outdoor = next(
      animal
      for animal in warm_day.animals
      if (
         animal.species == 'Aldabra Tortoise'
         and animal.enclosure_name == 'Outdoor' ) )
   assert outdoor.start_time is not None

   freeze_database_today( date( 2026, 7, 20 ) )
   # Later arrival cuts off packed guest stops so set_itinerary bulk-reschedules.
   result = ItineraryCoordinator.set_itinerary(
      date='2026-07-20',
      arrival_time='11:00',
      departure_time='17:00',
      animals=[
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
         ALDABRA_OUTDOOR_ENTRY,
         GORILLA_OUTDOOR_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      visit_date_temp=10,
   )

   assert result.success
   cool_day = ItineraryCoordinator.get_itinerary( visit_date_temp=10 )
   assert cool_day is not None

   outdoor_on_cool_day = [
      animal
      for animal in cool_day.animals
      if (
         animal.species == 'Aldabra Tortoise'
         and animal.enclosure_name == 'Outdoor' )
   ]
   assert outdoor_on_cool_day == []

   indoor = next(
      animal
      for animal in cool_day.animals
      if (
         animal.species == 'Aldabra Tortoise'
         and animal.enclosure_name == ALDABRA_INDOOR_ENCLOSURE ) )
   assert indoor.start_time is not None
   assert indoor.end_time is not None

   cheetah = next(
      animal
      for animal in cool_day.animals
      if animal.species == 'Cheetah' )
   gorilla = next(
      animal
      for animal in cool_day.animals
      if (
         animal.species == 'Western Lowland Gorilla'
         and animal.enclosure_name == 'Outdoor' ) )
   assert cheetah.start_time is not None
   assert cheetah.end_time is not None
   assert gorilla.start_time is not None
   assert all(
      animal.start_time is not None and animal.end_time is not None
      for animal in cool_day.animals )
