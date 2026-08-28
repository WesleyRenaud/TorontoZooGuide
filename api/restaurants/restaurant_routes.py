from __future__ import annotations

from .controllers.restaurant_controller import RestaurantController
from ..json_request_handler import PostRouteHandler


class RestaurantRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-restaurants': RestaurantController.get_restaurants,
   '/get-restaurant-names': RestaurantController.get_restaurant_names,
   '/set-restaurant-closed': RestaurantController.set_restaurant_closed,
   '/set-restaurant-closure-override': RestaurantController.set_restaurant_closure_override,
   '/set-restaurant-opening-schedule': RestaurantController.set_restaurant_opening_schedule,
   '/replace-restaurant-opening-schedule-overlaps': (
      RestaurantController.replace_restaurant_opening_schedule_overlaps
   ),
   '/trim-restaurant-opening-schedule-overlaps': (
      RestaurantController.trim_restaurant_opening_schedule_overlaps
   ),
}

