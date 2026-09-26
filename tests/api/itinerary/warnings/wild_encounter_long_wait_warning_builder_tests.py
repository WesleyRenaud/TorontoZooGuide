from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator import BulkRescheduleLongWaitSimulator
from api.itinerary.warnings.wild_encounter_long_wait_warning_builder import WildEncounterLongWaitWarningBuilder
from api.models import Animal
from api.models import WildEncounter
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType


RAINFOREST_ENCOUNTER = 'African Rainforest'
RHINO_ENCOUNTER = 'Guardians of White Rhinos'


def Test_IsolatedFromItinerary_TestEncounterFarFromItems_ExpectIsolatedEncounter() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   nearby_start = '10:15 AM'
   nearby_duration_minutes = 45
   far_start = '1:00 PM'
   far_duration_minutes = 45
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   nearby = WildEncounter(
      name=RAINFOREST_ENCOUNTER,
      meeting_spot='Wild Encounter - Africa Meeting Spot',
      link='',
      start_time=nearby_start,
      end_time=DateValues.add_minutes_to_time( nearby_start, nearby_duration_minutes ) )
   far = WildEncounter(
      name=RHINO_ENCOUNTER,
      meeting_spot='Wild Encounter - Penguin Meeting Spot',
      link='',
      start_time=far_start,
      end_time=DateValues.add_minutes_to_time( far_start, far_duration_minutes ) )
   itinerary.wild_encounters = [ nearby, far ]

   isolated = WildEncounterLongWaitWarningBuilder.isolated_from_itinerary( itinerary )

   assert [ encounter.name for encounter in isolated ] == [ far.name ]


def Test_IsolatedFromItinerary_TestEncounterNearItems_ExpectEmpty() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   encounter_start = '10:15 AM'
   encounter_duration_minutes = 45
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   itinerary.wild_encounters = [
      WildEncounter(
         name=RAINFOREST_ENCOUNTER,
         meeting_spot='Wild Encounter - Africa Meeting Spot',
         link='',
         start_time=encounter_start,
         end_time=DateValues.add_minutes_to_time(
            encounter_start,
            encounter_duration_minutes ) ),
   ]

   isolated = WildEncounterLongWaitWarningBuilder.isolated_from_itinerary( itinerary )

   assert isolated == []


def Test_ReasonAfterAddingWithSimulatedBulk_TestNotIsolated_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      'is_isolated_after_adding',
      lambda *args, **kwargs: False )
   encounter = WildEncounterDiff( name=RAINFOREST_ENCOUNTER, is_deleted=False )
   itinerary_context: dict = {}

   issue = WildEncounterLongWaitWarningBuilder.reason_after_adding_with_simulated_bulk(
      None,
      encounter,
      itinerary_context=itinerary_context )

   assert issue is None


def Test_ReasonAfterAddingWithSimulatedBulk_TestIsolated_ExpectIssue(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      'is_isolated_after_adding',
      lambda *args, **kwargs: True )
   start_time = '1:00 PM'
   duration_minutes = 30
   encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   itinerary_context: dict = {}

   issue = WildEncounterLongWaitWarningBuilder.reason_after_adding_with_simulated_bulk(
      None,
      encounter,
      itinerary_context=itinerary_context )

   assert issue is not None
   assert issue.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
