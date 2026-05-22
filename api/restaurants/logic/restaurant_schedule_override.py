class RestaurantScheduleOverride:
   def __init__(
         self,
         restaurant,
         start_date,
         end_date,
         is_closed,
         message ):
      self.restaurant = restaurant
      self.start_date = start_date
      self.end_date = end_date
      self.is_closed = is_closed
      self.message = message
