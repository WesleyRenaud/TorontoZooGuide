class AttractionScheduleOverride:
   def __init__(
         self,
         attraction,
         start_date,
         end_date,
         is_closed,
         message ):
      self.attraction = attraction
      self.start_date = start_date
      self.end_date = end_date
      self.is_closed = is_closed
      self.message = message
