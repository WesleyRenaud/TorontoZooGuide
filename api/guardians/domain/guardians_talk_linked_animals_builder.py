from __future__ import annotations

from ..data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from ...models import GuardiansTalk
from ...models.guardians_talk_linked_animal import GuardiansTalkLinkedAnimal
from ...types import Types


class GuardiansTalkLinkedAnimalsBuilder():
   @classmethod
   def attach(
         cls,
         conn: Types.Connection,
         talks: list[ GuardiansTalk ] ) -> list[ GuardiansTalk ]:
      for talk in talks:
         talk.linked_animals = [
            GuardiansTalkLinkedAnimal(
               species=link.species,
               exhibit=link.exhibit )
            for link in GuardiansTalkAnimalProvider.fetch_animal_links( conn, talk.name )
         ] if talk.name else []

      return talks
