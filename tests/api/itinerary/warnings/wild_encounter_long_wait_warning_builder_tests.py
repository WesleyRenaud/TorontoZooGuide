from __future__ import annotations

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.warnings.wild_encounter_long_wait_warning_builder import WildEncounterLongWaitWarningBuilder
from api.models import Animal
from api.models import WildEncounter
from api.shared.constants import Constants


RAINFOREST_ENCOUNTER = 'African Rainforest'
RHINO_ENCOUNTER = 'Guardians of White Rhinos'


def Test_IsolatedFromItinerary_TestEncounterFarFromItems_ExpectIsolatedEncounter() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.wild_encounters = [
      WildEncounter(
         name=RAINFOREST_ENCOUNTER,
         meeting_spot='Wild Encounter - Africa Meeting Spot',
         link='',
         start_time='10:15 AM',
         end_time='11:00 AM' ),
      WildEncounter(
         name=RHINO_ENCOUNTER,
         meeting_spot='Wild Encounter - Penguin Meeting Spot',
         link='',
         start_time='1:00 PM',
         end_time='1:45 PM' ),
   ]

   isolated = WildEncounterLongWaitWarningBuilder.isolated_from_itinerary( itinerary )

   assert [ encounter.name for encounter in isolated ] == [ RHINO_ENCOUNTER ]
   assert Constants.MAX_FIXED_TIME_ITEM_WAIT_MINUTES == 30


def Test_IsolatedFromItinerary_TestEncounterNearItems_ExpectEmpty() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.wild_encounters = [
      WildEncounter(
         name=RAINFOREST_ENCOUNTER,
         meeting_spot='Wild Encounter - Africa Meeting Spot',
         link='',
         start_time='10:15 AM',
         end_time='11:00 AM' ),
   ]

   assert WildEncounterLongWaitWarningBuilder.isolated_from_itinerary( itinerary ) == []
