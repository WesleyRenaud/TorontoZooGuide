from __future__ import annotations

from dataclasses import dataclass, field


@dataclass( frozen=True )
class GuardiansTalkOption:
   name: str
   enclosure_names: list[ str ] = field( default_factory=list )


   @classmethod
   def from_rows(
         cls,
         rows: list[ tuple[ str, str | None ] ] ) -> list[ GuardiansTalkOption ]:
      enclosure_names_by_name: dict[ str, list[ str ] ] = {}

      for name, enclosure_name in rows:
         enclosure_names = enclosure_names_by_name.setdefault( name, [] )

         if enclosure_name:
            enclosure_names.append( enclosure_name )

      return [
         cls( name=name, enclosure_names=enclosure_names )
         for name, enclosure_names in enclosure_names_by_name.items()
      ]


   def to_dict( self ) -> dict[ str, str | list[ str ] ]:
      return {
         'name': self.name,
         'enclosure_names': self.enclosure_names,
      }
