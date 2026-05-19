from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkNameFilter:
   name: object


   def __post_init__( self ):
      object.__setattr__(
         self,
         'name',
         ( self.name or '' ).strip().lower() )


   def should_return_empty( self ):
      return not self.name


   def allows_talk_name( self, name ):
      return ( name or '' ).strip().lower() == self.name
