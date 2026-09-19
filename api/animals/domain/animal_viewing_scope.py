from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class AnimalViewingScope:
   enclosure_name: str

   UNNAMED_LABEL = 'Main'


   @classmethod
   def from_enclosure_name( cls, name: str | None ) -> AnimalViewingScope:
      if name is None:
         return cls( enclosure_name='' )

      return cls( enclosure_name=name.strip() )


   @property
   def label( self ) -> str:
      return self.UNNAMED_LABEL if self.enclosure_name == '' else self.enclosure_name


   def to_dict( self ) -> dict[ str, str ]:
      return {
         'enclosureName': self.enclosure_name,
         'label': self.label,
      }
