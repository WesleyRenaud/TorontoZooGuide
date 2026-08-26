from __future__ import annotations

from api.guardians.domain.guardians_talk_linked_animals_builder import GuardiansTalkLinkedAnimalsBuilder
from api.models import GuardiansTalk
from api.models.guardians_talk_linked_animal import GuardiansTalkLinkedAnimal
from conftest import DbControllers


def test_attach_guardians_talk_linked_animals_uses_seeded_links(
      db: DbControllers ) -> None:
   assert db.conn is not None

   talks = GuardiansTalkLinkedAnimalsBuilder.attach(
      db.conn,
      [
         GuardiansTalk(
            name='African Lion',
            location='Africa Savanna',
            x_coord=0.0,
            y_coord=0.0 ),
         GuardiansTalk(
            name='New World Primates',
            location='Americas Pavilion',
            x_coord=0.0,
            y_coord=0.0 ),
         GuardiansTalk(
            name='Unmapped Talk',
            location='Nowhere',
            x_coord=0.0,
            y_coord=0.0 ),
      ] )

   assert talks[ 0 ].linked_animals == [
      GuardiansTalkLinkedAnimal(
         species='African Lion',
         exhibit='Africa Savanna' ),
   ]
   assert talks[ 1 ].linked_animals == [
      GuardiansTalkLinkedAnimal(
         species='Golden Lion Tamarin',
         exhibit='Americas Pavilion' ),
      GuardiansTalkLinkedAnimal(
         species='Two-Toed Sloth',
         exhibit='Americas Pavilion' ),
      GuardiansTalkLinkedAnimal(
         species='White-Faced Saki',
         exhibit='Americas Pavilion' ),
   ]
   assert talks[ 2 ].linked_animals == []
   assert talks[ 0 ].to_dict()[ 'linked_animals' ] == [
      {
         'species': 'African Lion',
         'exhibit': 'Africa Savanna',
      },
   ]
