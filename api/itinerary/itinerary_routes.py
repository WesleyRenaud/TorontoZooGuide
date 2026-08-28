from __future__ import annotations

from .controllers.itinerary_controller import ItineraryController
from ..json_request_handler import PostRouteHandler


class ItineraryRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/set-itinerary': ItineraryController.set_itinerary,
   '/get-itinerary-date': ItineraryController.get_itinerary_date,
   '/schedule-itinerary-item': ItineraryController.schedule_itinerary_item,
   '/bulk-schedule-itinerary': ItineraryController.bulk_schedule_itinerary,
   '/unschedule-all-itinerary-items': ItineraryController.unschedule_all_itinerary_items,
   '/unschedule-itinerary-item': ItineraryController.unschedule_itinerary_item,
   '/remove-item-from-itinerary': ItineraryController.remove_item_from_itinerary,
   '/set-itinerary-arrival-time': ItineraryController.set_itinerary_arrival_time,
   '/set-itinerary-departure-time': ItineraryController.set_itinerary_departure_time,
   '/suppress-itinerary-warning': ItineraryController.suppress_itinerary_warning,
   '/get-itinerary': ItineraryController.get_itinerary,
   '/clear-itinerary': ItineraryController.clear_itinerary,
   '/accept-itinerary': ItineraryController.accept_itinerary,
}

