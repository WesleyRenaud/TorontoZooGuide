from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterIncludeFilter:
   normalized_names: frozenset[ str ]
   provisioned_explicitly: bool


   @classmethod
   def from_optional_list( cls, wild_encounters_to_include=None ):
      if wild_encounters_to_include is None:
         return cls(
            normalized_names=frozenset(),
            provisioned_explicitly=False,
         )

      normalized_names = frozenset(
         wild_encounter_name.strip().lower()
         for wild_encounter_name in wild_encounters_to_include
      )

      return cls(
         normalized_names=normalized_names,
         provisioned_explicitly=True,
      )


   def should_return_empty( self ):
      return self.provisioned_explicitly and not self.normalized_names


   def allows_wild_encounter_name( self, name ):
      if not self.provisioned_explicitly:
         return True

      return ( name or '' ).strip().lower() in self.normalized_names
