from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterLink:
   name: str
   link: str


   @classmethod
   def stored_name( cls, name: str, encounters: list[ WildEncounterLink ] ) -> str:
      folded = name.casefold()

      for encounter in encounters:
         if encounter.name.casefold() == folded:
            return encounter.name

      return name


   @classmethod
   def booking_link( cls, name: str, encounters: list[ WildEncounterLink ] ) -> str:
      return next(
         encounter.link
         for encounter in encounters
         if encounter.name == name
      )
