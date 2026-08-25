from __future__ import annotations

from collections.abc import Callable
from typing import Any

from http_stub_controllers import StubControllerNamespace
from http_stub_controllers import StubZooControllers
from http_support_constants import ANIMAL_EXHIBIT
from http_support_constants import ANIMAL_NAME
from http_support_constants import ATTRACTION_NAME
from http_support_constants import GIFT_SHOP_NAME
from http_support_constants import GUARDIANS_TALK_LOCATION
from http_support_constants import GUARDIANS_TALK_NAME
from http_support_constants import PAVILION_NAME
from http_support_constants import REMOVED_ATTRACTION_NAME
from http_support_constants import RESTAURANT_NAME
from http_support_constants import RESTROOM_NAME
from http_support_constants import UPDATE_TITLE
from http_support_constants import WILD_ENCOUNTER_LINK
from http_support_constants import WILD_ENCOUNTER_MEETING_SPOT
from http_support_constants import WILD_ENCOUNTER_NAME
from http_support_constants import ZOOMOBILE_STATION_NAME
from http_support_handler import make_handler
from http_support_handler import response_json
import pytest

from api.types import Connection

def _patch_controller_with_stub(
      monkeypatch: pytest.MonkeyPatch,
      controller_class: type,
      stub: StubZooControllers ) -> None:
   for method_name in dir( controller_class ):
      if method_name.startswith( '_' ) or not hasattr( stub, method_name ):
         continue

      stub_method = getattr( stub, method_name )

      if not callable( stub_method ):
         continue

      @classmethod
      def patched( cls: type, *args: Any, _stub_method: Callable[ ..., Any ] = stub_method, **kwargs: Any ) -> Any:
         return _stub_method( *args, **kwargs )

      monkeypatch.setattr( controller_class, method_name, patched )

@pytest.fixture
def stub_controllers( monkeypatch: pytest.MonkeyPatch ) -> type[ StubZooControllers ]:
   from api import connection
   from api.animals.coordinators.animal_coordinator import AnimalCoordinator
   from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
   from api.defibrillators.coordinators.defibrillator_coordinator import DefibrillatorCoordinator
   from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
   from api.emergency_intercoms.coordinators.emergency_intercom_coordinator import EmergencyIntercomCoordinator
   from api.event_sites.coordinators.event_site_coordinator import EventSiteCoordinator
   from api.events.coordinators.event_coordinator import EventCoordinator
   from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
   from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
   from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
   from api.guest_services.coordinators.guest_service_coordinator import GuestServiceCoordinator
   from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
   from api.pavilions.coordinators.pavilion_coordinator import PavilionCoordinator
   from api.picnic_sites.coordinators.picnic_site_coordinator import PicnicSiteCoordinator
   import api.request_connection as request_connection
   from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
   from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
   from api.transportation.coordinators.transportation_coordinator import TransportationCoordinator
   from api.updates.coordinators.update_coordinator import UpdateCoordinator
   from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
   from api.zoo_hours.coordinators.zoo_hours_coordinator import ZooHoursCoordinator

   StubZooControllers.instances = []
   StubZooControllers.default_success = True
   stub = StubZooControllers( None )

   monkeypatch.setattr( connection, 'open_connection', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Connection | None ) -> None:
      StubZooControllers._active = stub

   def stub_clear_connection() -> None:
      if StubZooControllers.instances:
         StubZooControllers.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection, 'set_connection', stub_set_connection )
   monkeypatch.setattr( request_connection, 'clear_connection', stub_clear_connection )

   controller_classes = [
      AnimalCoordinator,
      ExhibitCoordinator,
      PavilionCoordinator,
      RestaurantCoordinator,
      RestroomCoordinator,
      GiftShopCoordinator,
      AttractionCoordinator,
      TransportationCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      DrinkingFountainCoordinator,
      DefibrillatorCoordinator,
      EmergencyIntercomCoordinator,
      GuestServiceCoordinator,
      PicnicSiteCoordinator,
      EventSiteCoordinator,
      EventCoordinator,
      UpdateCoordinator,
      ItineraryCoordinator,
      ZooHoursCoordinator,
   ]

   for controller_class in controller_classes:
      _patch_controller_with_stub( monkeypatch, controller_class, stub )

   return StubZooControllers

@pytest.fixture
def stub_database( stub_controllers: type[ StubZooControllers ] ) -> type[ StubZooControllers ]:
   return stub_controllers
