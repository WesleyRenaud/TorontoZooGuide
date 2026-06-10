from __future__ import annotations

from .controllers.itinerary_controller import ItineraryController
from ..json_handler import PostRouteHandler


ITINERARY_ROUTES: dict[ str, PostRouteHandler ] = {
   '/set-itinerary': ItineraryController.set_itinerary,
   '/get-itinerary-date': ItineraryController.get_itinerary_date,
   '/schedule-itinerary-item': ItineraryController.schedule_itinerary_item,
   '/bulk-schedule-animals': ItineraryController.bulk_schedule_animals,
   '/unschedule-itinerary-item': ItineraryController.unschedule_itinerary_item,
   '/remove-item-from-itinerary': ItineraryController.remove_item_from_itinerary,
   '/set-itinerary-arrival-time': ItineraryController.set_itinerary_arrival_time,
   '/set-itinerary-departure-time': ItineraryController.set_itinerary_departure_time,
   '/suppress-itinerary-warning': ItineraryController.suppress_itinerary_warning,
   '/get-itinerary': ItineraryController.get_itinerary,
   '/clear-itinerary': ItineraryController.clear_itinerary,
   '/accept-itinerary': ItineraryController.accept_itinerary,
}
