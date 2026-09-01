from __future__ import annotations

import pytest

from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.models import WildEncounter
from api.shared.enums import ScheduleItemKind
from api.walk_graph.domain.master_route_loop import MasterRouteLoop
from api.walk_graph.domain.master_route_loop import ONE_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference
from api.walk_graph.master_route_provider import MasterRouteProvider
from api.wild_encounters.data_access.wild_encounter_meeting_spot_loop_pin_record import WildEncounterMeetingSpotLoopPinRecord
from api.wild_encounters.scheduling.wild_encounter_loop_schedule_pin_resolver import WildEncounterLoopSchedulePinResolver


CANADIAN_DOMAIN_MEETING_SPOT = 'Wild Encounter - Canadian Domain Meeting Spot'
MAYAN_TEMPLE_MEETING_SPOT = 'Wild Encounter - Mayan Temple Meeting Spot'
PENGUIN_MEETING_SPOT = 'Wild Encounter - Penguin Meeting Spot'
EURASIA_MEETING_SPOT = 'Wild Encounter - Eurasia Meeting Spot'
BACTRIAN_CAMELS_ENCOUNTER = 'Bactrian Camels'
CANADIAN_DOMAIN_SAVANNA_LOOP_ID = 'africa_savanna_canadian_domain'
TUNDRA_TREK_MAYAN_TEMPLE_LOOP_ID = 'tundra_trek_mayan_temple'
GRIZZLY_BEAR_ENCOUNTER = 'Grizzly Bear'
CANADIAN_DOMAIN_PIN_INDEX = 6
MAYAN_TEMPLE_PIN_INDEX = 3


def _viewing_spot(
      *,
      species: str,
      exhibit: str,
      name: str | None = None ) -> ViewingSpotReference:
   return ViewingSpotReference(
      species=species,
      exhibit=exhibit,
      name=name )


CANADIAN_DOMAIN_SAVANNA_MASTER_ROUTE_LOOP = MasterRouteLoop(
   loop_id=CANADIAN_DOMAIN_SAVANNA_LOOP_ID,
   name='Africa Savanna',
   traversal=ONE_WAY_LOOP_TRAVERSAL,
   viewing_spots=[
      *[
         _viewing_spot(
            species=f'Placeholder { index }',
            exhibit='Africa Savanna' )
         for index in range( CANADIAN_DOMAIN_PIN_INDEX )
      ],
      _viewing_spot(
         species="Grevy's Zebra",
         exhibit='Canadian Domain' ),
      _viewing_spot(
         species='Raccoon',
         exhibit='Canadian Domain' ),
   ],
)

TUNDRA_MAYAN_TEMPLE_LOOP = MasterRouteLoop(
   loop_id=TUNDRA_TREK_MAYAN_TEMPLE_LOOP_ID,
   name='Tundra Trek Mayan Temple',
   traversal=ONE_WAY_LOOP_TRAVERSAL,
   viewing_spots=[
      *[
         _viewing_spot(
            species=f'Placeholder { index }',
            exhibit='Tundra Trek' )
         for index in range( MAYAN_TEMPLE_PIN_INDEX )
      ],
      _viewing_spot(
         species='Capybara',
         exhibit='Americas Outdoor Mayan Temple Ruins' ),
   ],
)

LOOPS_BY_ID = {
   CANADIAN_DOMAIN_SAVANNA_LOOP_ID: CANADIAN_DOMAIN_SAVANNA_MASTER_ROUTE_LOOP,
   TUNDRA_TREK_MAYAN_TEMPLE_LOOP_ID: TUNDRA_MAYAN_TEMPLE_LOOP,
}

MEETING_SPOT_LOOP_PINS = {
   CANADIAN_DOMAIN_MEETING_SPOT: WildEncounterMeetingSpotLoopPinRecord(
      name=CANADIAN_DOMAIN_MEETING_SPOT,
      loop_id=CANADIAN_DOMAIN_SAVANNA_LOOP_ID,
      loop_viewing_spot_index=CANADIAN_DOMAIN_PIN_INDEX ),
   MAYAN_TEMPLE_MEETING_SPOT: WildEncounterMeetingSpotLoopPinRecord(
      name=MAYAN_TEMPLE_MEETING_SPOT,
      loop_id=TUNDRA_TREK_MAYAN_TEMPLE_LOOP_ID,
      loop_viewing_spot_index=MAYAN_TEMPLE_PIN_INDEX ),
}


def _wild_encounter_stop(
      *,
      item_key: str,
      meeting_spot: str,
      start_time: str,
      end_time: str ) -> ItineraryStop:
   return ItineraryStop(
      schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
      item_key=item_key,
      meeting_spot=meeting_spot,
      walk_node_ids=( 'v-0001', ),
      is_fixed_time=True,
      start_time=start_time,
      end_time=end_time )


@pytest.fixture
def stub_wild_encounter_loop_schedule_pin_resolver(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MasterRouteProvider,
      'loops_by_id',
      lambda: LOOPS_BY_ID )


def Test_Resolve_TestUnpinnedMeetingSpot_ExpectNone(
      stub_wild_encounter_loop_schedule_pin_resolver: None ) -> None:
   wild_encounter = WildEncounter(
      name='Guardians of White Rhinos',
      meeting_spot=PENGUIN_MEETING_SPOT,
      link='https://example.com',
      x_coord=0.0,
      y_coord=0.0,
      start_time='10:00 AM',
      end_time='10:45 AM' )

   assert WildEncounterLoopSchedulePinResolver.resolve(
      wild_encounter,
      _wild_encounter_stop(
         item_key='Guardians of White Rhinos',
         meeting_spot=PENGUIN_MEETING_SPOT,
         start_time='10:00 AM',
         end_time='10:45 AM' ),
      meeting_spot_loop_pins_by_name=MEETING_SPOT_LOOP_PINS ) is None


def Test_Resolve_TestBactrianCamelsEurasiaMeetingSpot_ExpectNone(
      stub_wild_encounter_loop_schedule_pin_resolver: None ) -> None:
   wild_encounter = WildEncounter(
      name=BACTRIAN_CAMELS_ENCOUNTER,
      meeting_spot=EURASIA_MEETING_SPOT,
      link='https://example.com',
      x_coord=0.0,
      y_coord=0.0,
      start_time='3:30 PM',
      end_time='4:00 PM' )

   assert WildEncounterLoopSchedulePinResolver.resolve(
      wild_encounter,
      _wild_encounter_stop(
         item_key=BACTRIAN_CAMELS_ENCOUNTER,
         meeting_spot=EURASIA_MEETING_SPOT,
         start_time='3:30 PM',
         end_time='4:00 PM' ),
      meeting_spot_loop_pins_by_name=MEETING_SPOT_LOOP_PINS ) is None


def Test_Resolve_TestCanadianDomainMeetingSpot_ExpectSavannaLoopPin(
      stub_wild_encounter_loop_schedule_pin_resolver: None ) -> None:
   wild_encounter = WildEncounter(
      name=GRIZZLY_BEAR_ENCOUNTER,
      meeting_spot=CANADIAN_DOMAIN_MEETING_SPOT,
      link='https://example.com',
      x_coord=0.0,
      y_coord=0.0,
      start_time='1:00 PM',
      end_time='1:45 PM' )
   master_route_loop = LOOPS_BY_ID[ CANADIAN_DOMAIN_SAVANNA_LOOP_ID ]

   loop_pin = WildEncounterLoopSchedulePinResolver.resolve(
      wild_encounter,
      _wild_encounter_stop(
         item_key=GRIZZLY_BEAR_ENCOUNTER,
         meeting_spot=CANADIAN_DOMAIN_MEETING_SPOT,
         start_time='1:00 PM',
         end_time='1:45 PM' ),
      meeting_spot_loop_pins_by_name=MEETING_SPOT_LOOP_PINS )

   assert loop_pin is not None
   assert loop_pin.loop_id == CANADIAN_DOMAIN_SAVANNA_LOOP_ID
   assert loop_pin.viewing_spot_index == CANADIAN_DOMAIN_PIN_INDEX
   assert (
         master_route_loop.viewing_spots[ CANADIAN_DOMAIN_PIN_INDEX ].species
         == "Grevy's Zebra" )
   assert master_route_loop.viewing_spots[ CANADIAN_DOMAIN_PIN_INDEX + 1 ].species == (
      'Raccoon' )


def Test_Resolve_TestMayanTempleMeetingSpot_ExpectTundraLoopPin(
      stub_wild_encounter_loop_schedule_pin_resolver: None ) -> None:
   for encounter_name in ( 'Capybara', 'From Howls to Honks' ):
      wild_encounter = WildEncounter(
         name=encounter_name,
         meeting_spot=MAYAN_TEMPLE_MEETING_SPOT,
         link='https://example.com',
         x_coord=0.0,
         y_coord=0.0,
         start_time='11:00 AM',
         end_time='11:30 AM' )

      loop_pin = WildEncounterLoopSchedulePinResolver.resolve(
         wild_encounter,
         _wild_encounter_stop(
            item_key=encounter_name,
            meeting_spot=MAYAN_TEMPLE_MEETING_SPOT,
            start_time='11:00 AM',
            end_time='11:30 AM' ),
         meeting_spot_loop_pins_by_name=MEETING_SPOT_LOOP_PINS )

      assert loop_pin is not None
      assert loop_pin.loop_id == TUNDRA_TREK_MAYAN_TEMPLE_LOOP_ID
      assert loop_pin.viewing_spot_index == MAYAN_TEMPLE_PIN_INDEX


def Test_Resolve_TestMissingMasterRouteLoop_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MasterRouteProvider,
      'loops_by_id',
      lambda: {} )

   wild_encounter = WildEncounter(
      name=GRIZZLY_BEAR_ENCOUNTER,
      meeting_spot=CANADIAN_DOMAIN_MEETING_SPOT,
      link='https://example.com',
      x_coord=0.0,
      y_coord=0.0,
      start_time='1:00 PM',
      end_time='1:45 PM' )

   assert WildEncounterLoopSchedulePinResolver.resolve(
      wild_encounter,
      _wild_encounter_stop(
         item_key=GRIZZLY_BEAR_ENCOUNTER,
         meeting_spot=CANADIAN_DOMAIN_MEETING_SPOT,
         start_time='1:00 PM',
         end_time='1:45 PM' ),
      meeting_spot_loop_pins_by_name=MEETING_SPOT_LOOP_PINS ) is None
