from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkIncludeFilter:
   """Which talk names may appear in a details response (``None`` = all talks)."""
   normalized_names: frozenset[ str ]
   provisioned_explicitly: bool


   @classmethod
   def from_optional_list(
         cls,
         guardians_talks_to_include: list[ str ] | None ) -> GuardiansTalkIncludeFilter:
      if guardians_talks_to_include is None:
         return cls(
            normalized_names=frozenset(),
            provisioned_explicitly=False,
         )

      normalized_names = frozenset(
         talk_name.strip().lower()
         for talk_name in guardians_talks_to_include
      )

      return cls(
         normalized_names=normalized_names,
         provisioned_explicitly=True,
      )


   def should_return_empty( self ) -> bool:
      return self.provisioned_explicitly and not self.normalized_names


   def allows_talk_name( self, name: str | None ) -> bool:
      if not self.provisioned_explicitly:
         return True

      return ( name or '' ).strip().lower() in self.normalized_names
