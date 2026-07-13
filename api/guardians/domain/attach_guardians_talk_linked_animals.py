from __future__ import annotations

from ..data_access.guardians_talk_animal import fetch_guardians_talk_animal_links
from ...models import GuardiansTalk
from ...models.guardians_talk_linked_animal import GuardiansTalkLinkedAnimal
from ...types import Connection


def attach_guardians_talk_linked_animals(
      conn: Connection,
      talks: list[ GuardiansTalk ] ) -> list[ GuardiansTalk ]:
   for talk in talks:
      talk.linked_animals = [
         GuardiansTalkLinkedAnimal(
            species=link.species,
            exhibit=link.exhibit )
         for link in fetch_guardians_talk_animal_links( conn, talk.name )
      ] if talk.name else []

   return talks
