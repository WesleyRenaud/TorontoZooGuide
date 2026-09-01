from __future__ import annotations

from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.itinerary_routes import ItineraryRoutes


def Test_Routes_TestRegisteredPaths_ExpectItineraryControllerHandlers() -> None:
   assert ItineraryRoutes.ROUTES[ '/set-itinerary' ] is ItineraryController.set_itinerary
   assert ItineraryRoutes.ROUTES[ '/get-itinerary' ] is ItineraryController.get_itinerary
   assert ItineraryRoutes.ROUTES[ '/schedule-itinerary-item' ] is (
      ItineraryController.schedule_itinerary_item )
   assert ItineraryRoutes.ROUTES[ '/bulk-schedule-itinerary' ] is (
      ItineraryController.bulk_schedule_itinerary )
   assert ItineraryRoutes.ROUTES[ '/unschedule-itinerary-item' ] is (
      ItineraryController.unschedule_itinerary_item )
   assert ItineraryRoutes.ROUTES[ '/clear-itinerary' ] is ItineraryController.clear_itinerary
   assert ItineraryRoutes.ROUTES[ '/accept-itinerary' ] is ItineraryController.accept_itinerary


def Test_Routes_TestAllPaths_ExpectThirteenHandlers() -> None:
   assert len( ItineraryRoutes.ROUTES ) == 13
   assert all( callable( handler ) for handler in ItineraryRoutes.ROUTES.values() )
