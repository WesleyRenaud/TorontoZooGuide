from __future__ import annotations

from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.wild_encounter_item_key import WildEncounterScheduleItemKey


def test_wild_encounter_schedule_item_key_from_wire_without_time() -> None:
   assert WildEncounterScheduleItemKey.from_wire( 'African Rainforest' ) is None
   assert WildEncounterScheduleItemKey.from_wire( 'African Rainforest||' ) is None
   assert WildEncounterScheduleItemKey.from_wire( 'Kangaroo||1:00 PM||' ) is None
   assert WildEncounterScheduleItemKey.from_wire( 'Kangaroo||1:00 PM||bad' ) is None


def test_wild_encounter_schedule_item_key_from_wire_with_start_time() -> None:
   key = WildEncounterScheduleItemKey.from_wire( 'Masai Giraffe||14:00' )

   assert key == WildEncounterScheduleItemKey(
      name='Masai Giraffe',
      start_time='2:00 PM' )
   assert key.to_wire() == 'Masai Giraffe||2:00 PM'


def test_wild_encounter_schedule_item_key_from_wire_with_start_and_end_time() -> None:
   key = WildEncounterScheduleItemKey.from_wire( 'Kangaroo||13:00||13:45' )

   assert key == WildEncounterScheduleItemKey(
      name='Kangaroo',
      start_time='1:00 PM',
      end_time='1:45 PM' )
   assert key.to_wire() == 'Kangaroo||1:00 PM||1:45 PM'


def test_wild_encounter_schedule_item_key_from_wires() -> None:
   keys = WildEncounterScheduleItemKey.from_wires( [
      'Kangaroo||13:00||13:45',
      '',
      'Capybara',
      'Capybara||11:00',
   ] )

   assert keys == [
      WildEncounterScheduleItemKey(
         name='Kangaroo',
         start_time='1:00 PM',
         end_time='1:45 PM' ),
      WildEncounterScheduleItemKey(
         name='Capybara',
         start_time='11:00 AM' ),
   ]


def test_wild_encounter_schedule_item_key_from_row() -> None:
   record = ItineraryWildEncounterRecord(
      wild_encounter='Kangaroo',
      start_time='13:00',
      end_time='13:45',
      is_deleted=False,
   )

   assert record.schedule_item_key() == WildEncounterScheduleItemKey(
      name='Kangaroo',
      start_time='1:00 PM',
      end_time='1:45 PM' )
   assert record.schedule_item_key().to_wire() == 'Kangaroo||1:00 PM||1:45 PM'
