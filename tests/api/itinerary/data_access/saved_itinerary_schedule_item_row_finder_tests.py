from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.shared.date_values import DateValues
from api.shared.enums import ItineraryEventType
from api.shared.enums.transportation_name import TransportationName


VISIT_DATE = '2026-06-15'


def Test_FindSavedItineraryScheduleItemRow_TestAnimalKey_ExpectAnimalRow() -> None:
   species = 'Masai Giraffe'
   exhibit = 'Africa Savanna'
   start_time = '10:15 AM'
   duration_minutes = 15
   animal_row = ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      animal_rows=( animal_row, ),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=() )
   schedule_item_key = AnimalScheduleItemKey(
      species=species,
      exhibit=exhibit )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert row is not None
   assert row.species == animal_row.species


def Test_FindSavedItineraryScheduleItemRow_TestAttractionKey_ExpectAttractionRow() -> None:
   attraction = 'Conservation Carousel'
   attraction_row = ItineraryAttractionRecord(
      attraction=attraction,
      old_likelihood=None,
      new_likelihood=None )
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=( attraction_row, ),
      guardians_talk_rows=(),
      wild_encounter_rows=() )
   schedule_item_key = AttractionScheduleItemKey( name=attraction )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert row is not None
   assert row.attraction == attraction_row.attraction


def Test_FindSavedItineraryScheduleItemRow_TestAttractionTransport_ExpectAttractionModeRow() -> None:
   transportation = TransportationName.ZOOMOBILE
   attraction_mode_row = ItineraryTransportationRecord(
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=3,
      added_as_attraction=True )
   transit_row = ItineraryTransportationRecord(
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=3,
      added_as_attraction=False )
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      transportation_rows=( attraction_mode_row, transit_row ) )
   schedule_item_key = AttractionScheduleItemKey( name=transportation )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert isinstance( row, ItineraryTransportationRecord )
   assert row.added_as_attraction is attraction_mode_row.added_as_attraction


def Test_FindSavedItineraryScheduleItemRow_TestPureTransportAsAttraction_ExpectNone() -> None:
   transportation = TransportationName.ZOOMOBILE
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      transportation_rows=(
         ItineraryTransportationRecord(
            transportation=transportation,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False ),
      ) )
   schedule_item_key = AttractionScheduleItemKey( name=transportation )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert row is None


def Test_FindSavedItineraryScheduleItemRow_TestTransportationKey_ExpectTransitRow() -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = False
   attraction_mode_row = ItineraryTransportationRecord(
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=3,
      added_as_attraction=True )
   transit_row = ItineraryTransportationRecord(
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=3,
      added_as_attraction=added_as_attraction )
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      transportation_rows=( attraction_mode_row, transit_row ) )
   schedule_item_key = TransportationScheduleItemKey(
      name=transportation,
      added_as_attraction=added_as_attraction )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert isinstance( row, ItineraryTransportationRecord )
   assert row.added_as_attraction is added_as_attraction


def Test_FindSavedItineraryScheduleItemRow_TestEventType_ExpectEventRow() -> None:
   event_type = ItineraryEventType.LUNCH
   start_time = '12:00 PM'
   duration_minutes = 30
   event_row = ItineraryEventRecord(
      event_type=event_type,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=(),
      event_rows=( event_row, ) )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      event_type )

   assert row is not None
   assert row.event_type == event_row.event_type


def Test_FindSavedItineraryScheduleItemRow_TestWildEncounterKey_ExpectMatchingStart() -> None:
   encounter_name = 'African Rainforest'
   start_time = '3:30 PM'
   duration_minutes = 45
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   encounter_row = ItineraryWildEncounterRecord(
      wild_encounter=encounter_name,
      start_time=start_time,
      end_time=end_time,
      is_deleted=False )
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=( encounter_row, ) )
   schedule_item_key = WildEncounterScheduleItemKey(
      name=encounter_name,
      start_time=DateValues.format_time_value( start_time ) )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert row is not None
   assert row.wild_encounter == encounter_row.wild_encounter
   assert row.end_time == encounter_row.end_time


def Test_FindSavedItineraryScheduleItemRow_TestWildEncounterDifferentStart_ExpectNone() -> None:
   encounter_name = 'African Rainforest'
   start_time = '3:30 PM'
   duration_minutes = 45
   other_start_time = '2:00 PM'
   encounter_row = ItineraryWildEncounterRecord(
      wild_encounter=encounter_name,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      is_deleted=False )
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=( encounter_row, ) )
   schedule_item_key = WildEncounterScheduleItemKey(
      name=encounter_name,
      start_time=DateValues.format_time_value( other_start_time ) )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert row is None


def Test_SavedScheduleItemIsAlreadyScheduled_TestScheduledAnimal_ExpectTrue() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   start_time = '10:00 AM'
   duration_minutes = 8
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species=species,
            exhibit=exhibit,
            start_time=start_time,
            end_time=DateValues.add_minutes_to_time(
               start_time,
               duration_minutes ) ),
      ] )
   schedule_item_key = AnimalScheduleItemKey(
      species=species,
      exhibit=exhibit )

   is_scheduled = SavedItineraryScheduleItemRowFinder.saved_schedule_item_is_already_scheduled(
      saved_itinerary,
      schedule_item_key )

   assert is_scheduled


def Test_SavedScheduleItemIsAlreadyScheduled_TestUnscheduledAnimal_ExpectFalse() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species=species,
            exhibit=exhibit ),
      ] )
   schedule_item_key = AnimalScheduleItemKey(
      species=species,
      exhibit=exhibit )

   is_scheduled = SavedItineraryScheduleItemRowFinder.saved_schedule_item_is_already_scheduled(
      saved_itinerary,
      schedule_item_key )

   assert not is_scheduled


def Test_SavedScheduleItemIsAlreadyScheduled_TestScheduledLunch_ExpectTrue() -> None:
   event_type = ItineraryEventType.LUNCH
   start_time = '12:00 PM'
   duration_minutes = 40
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      event_rows=[
         ItineraryEventRecord(
            event_type=event_type,
            start_time=start_time,
            end_time=DateValues.add_minutes_to_time(
               start_time,
               duration_minutes ) ),
      ] )

   is_scheduled = SavedItineraryScheduleItemRowFinder.saved_schedule_item_is_already_scheduled(
      saved_itinerary,
      event_type )

   assert is_scheduled


def Test_FindSavedItineraryScheduleItemRow_TestDeletedGuardiansTalk_ExpectNone() -> None:
   talk_name = 'African Lion'
   start_time = '2:00 PM'
   duration_minutes = 30
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name=talk_name,
            start_time=start_time,
            end_time=DateValues.add_minutes_to_time(
               start_time,
               duration_minutes ),
            is_deleted=True ),
      ] )
   schedule_item_key = GuardiansTalkScheduleItemKey(
      name=talk_name,
      start_time=start_time )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert row is None


def Test_FindSavedItineraryScheduleItemRow_TestDeletedWildEncounter_ExpectNone() -> None:
   encounter_name = 'Kangaroo'
   start_time = '1:00 PM'
   duration_minutes = 45
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None,
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter=encounter_name,
            start_time=start_time,
            end_time=DateValues.add_minutes_to_time(
               start_time,
               duration_minutes ),
            is_deleted=True ),
      ] )
   schedule_item_key = WildEncounterScheduleItemKey(
      name=encounter_name,
      start_time=start_time )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert row is None


def Test_FindSavedItineraryScheduleItemRow_TestUnknownKeyType_ExpectNone() -> None:
   class UnknownScheduleItemKey:
      pass

   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=None,
      departure_time=None )
   schedule_item_key = UnknownScheduleItemKey()

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )  # type: ignore[arg-type]

   assert row is None
