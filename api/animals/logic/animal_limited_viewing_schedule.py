class AnimalLimitedViewingSchedule:
   def __init__(
         self,
         species,
         exhibit,
         start_date,
         end_date,
         daily_start_time,
         daily_end_time,
         message ):
      self.species = species
      self.exhibit = exhibit
      self.start_date = start_date
      self.end_date = end_date
      self.daily_start_time = daily_start_time
      self.daily_end_time = daily_end_time
      self.message = message
