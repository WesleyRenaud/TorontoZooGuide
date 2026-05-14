class Update:
   def __init__( self, title, description, update_type, start_date, end_date ):
      self.title = title
      self.description = description
      self.update_type = update_type
      self.start_date = start_date
      self.end_date = end_date


   def to_dict( self ):
      return {
         'title': self.title,
         'description': self.description,
         'type': self.update_type,
         'start_date': self.start_date,
         'end_date': self.end_date
      }
