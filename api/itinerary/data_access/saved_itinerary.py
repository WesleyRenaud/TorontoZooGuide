from dataclasses import dataclass

from ... import zoo


@dataclass( frozen=True )
class SavedItinerary:
   date_value: object
   animal_rows: tuple
   attraction_rows: tuple
   guardians_talk_rows: tuple
   wild_encounter_rows: tuple


   def is_empty( self ):
      return self.date_value == None


   def itinerary_date( self ):
      return zoo.ZooUtil.parse_date_value( self.date_value )


   def month( self ):
      return self.itinerary_date().month


   def day( self ):
      return self.itinerary_date().day


   def year( self ):
      return self.itinerary_date().year


   def species_exhibit_pairs( self ):
      return [
         animal.species_exhibit_key()
         for animal in self.animal_rows
      ]


   def attraction_names( self ):
      return [
         attraction.attraction
         for attraction in self.attraction_rows
      ]


   def guardians_talk_names( self ):
      return [
         talk.talk_name
         for talk in self.guardians_talk_rows
      ]


   def wild_encounter_names( self ):
      return [
         encounter.wild_encounter
         for encounter in self.wild_encounter_rows
      ]
