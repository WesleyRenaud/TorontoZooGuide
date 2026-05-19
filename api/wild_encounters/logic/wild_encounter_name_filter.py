from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterNameFilter:
   name: object


   def __post_init__( self ):
      object.__setattr__(
         self,
         'name',
         ( self.name or '' ).strip().lower() )


   def should_return_empty( self ):
      return not self.name


   def allows_wild_encounter_name( self, name ):
      return ( name or '' ).strip().lower() == self.name
