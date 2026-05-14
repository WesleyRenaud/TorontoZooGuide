class Itinerary:
   def __init__( self, date, animals=[], attractions=[], guardians_talks=[], wild_encounters=[] ):
      self.date = date
      self.animals = animals
      self.attractions = attractions
      self.guardians_talks = guardians_talks
      self.wild_encounters = wild_encounters


   def to_dict( self ):
      return {
         'date': self.date,
         'animals': [
            self._to_dict_with_type( a, 'animal' ) for a in self.animals
         ],
         'attractions': [
            self._to_dict_with_type( a, 'attraction' ) for a in self.attractions
         ],
         'guardians_talks': [
            self._to_dict_with_type( g, 'guardiansTalk' ) for g in self.guardians_talks
         ],
         'wild_encounters': [
            self._to_dict_with_type( w, 'wildEncounter' ) for w in self.wild_encounters
         ]
      }


   def _to_dict_with_type( self, obj, fallback_type ):
      if hasattr( obj, 'to_dict' ):
         d = obj.to_dict()
      else:
         d = dict( obj ) if isinstance( obj, dict ) else {}

      d[ 'type' ] = d.get( 'type', fallback_type )
      return d
