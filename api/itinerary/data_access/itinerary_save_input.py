from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class ItinerarySaveInput:
   date: date
   animals: tuple
   attractions: tuple
   guardians_talks: tuple
   wild_encounters: tuple


   def month( self ):
      return self.date.month


   def day( self ):
      return self.date.day


   def year( self ):
      return self.date.year
