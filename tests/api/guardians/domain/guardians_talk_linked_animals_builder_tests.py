from __future__ import annotations

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from api.guardians.data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from api.guardians.domain.guardians_talk_linked_animals_builder import GuardiansTalkLinkedAnimalsBuilder
from api.models.guardians_talk import GuardiansTalk
from api.models.guardians_talk_linked_animal import GuardiansTalkLinkedAnimal
from api.types import Types

STATION_COORD = 0.0

AFRICAN_LION_TALK = 'African Lion'
NEW_WORLD_PRIMATES_TALK = 'New World Primates'
UNMAPPED_TALK = 'Unmapped Talk'


def _talk( name: str, location: str ) -> GuardiansTalk:
   return GuardiansTalk(
      name=name,
      location=location,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD )


def _animal_links_by_talk() -> dict[ str, list[ GuardiansTalkAnimalRecord ] ]:
   return {
      AFRICAN_LION_TALK: [
         GuardiansTalkAnimalRecord(
            talk_name=AFRICAN_LION_TALK,
            location='Africa Savanna',
            species='African Lion',
            exhibit='Africa Savanna' ),
      ],
      NEW_WORLD_PRIMATES_TALK: [
         GuardiansTalkAnimalRecord(
            talk_name=NEW_WORLD_PRIMATES_TALK,
            location='Americas Pavilion',
            species='Golden Lion Tamarin',
            exhibit='Americas Pavilion' ),
         GuardiansTalkAnimalRecord(
            talk_name=NEW_WORLD_PRIMATES_TALK,
            location='Americas Pavilion',
            species='Two-Toed Sloth',
            exhibit='Americas Pavilion' ),
         GuardiansTalkAnimalRecord(
            talk_name=NEW_WORLD_PRIMATES_TALK,
            location='Americas Pavilion',
            species='White-Faced Saki',
            exhibit='Americas Pavilion' ),
      ],
   }


def Test_Attach_TestLinkedTalks_ExpectMappedLinkedAnimals(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   links_by_talk = _animal_links_by_talk()

   def fetch_animal_links(
         _conn: Types.Connection,
         talk_name: str ) -> list[ GuardiansTalkAnimalRecord ]:
      return links_by_talk.get( talk_name, [] )

   monkeypatch.setattr(
      GuardiansTalkAnimalProvider,
      'fetch_animal_links',
      fetch_animal_links )

   talks = GuardiansTalkLinkedAnimalsBuilder.attach(
      conn=STUB_REQUEST_CONNECTION,
      talks=[
         _talk( AFRICAN_LION_TALK, 'Africa Savanna' ),
         _talk( NEW_WORLD_PRIMATES_TALK, 'Americas Pavilion' ),
         _talk( UNMAPPED_TALK, 'Nowhere' ),
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


def Test_Attach_TestMissingTalkName_ExpectEmptyLinkedAnimals() -> None:
   talk = GuardiansTalk(
      name='',
      location='Nowhere',
      x_coord=STATION_COORD,
      y_coord=STATION_COORD )

   talks = GuardiansTalkLinkedAnimalsBuilder.attach( conn=STUB_REQUEST_CONNECTION, talks=[ talk ] )

   assert talks[ 0 ].linked_animals == []
