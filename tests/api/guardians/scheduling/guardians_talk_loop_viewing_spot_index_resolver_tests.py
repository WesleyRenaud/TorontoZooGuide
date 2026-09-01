from __future__ import annotations

from api.guardians.data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from api.guardians.scheduling.guardians_talk_loop_viewing_spot_index_resolver import GuardiansTalkLoopViewingSpotIndexResolver
from api.walk_graph.domain.master_route_loop import MasterRouteLoop
from api.walk_graph.domain.master_route_loop import ONE_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference


AFRICA_SAVANNA_LOOP = MasterRouteLoop(
   loop_id='africa_savanna_canadian_domain',
   name='Africa Savanna',
   traversal=ONE_WAY_LOOP_TRAVERSAL,
   viewing_spots=[
      ViewingSpotReference(
         species='African Lion',
         exhibit='Africa Savanna',
         name=None ),
      ViewingSpotReference(
         species='African Penguin',
         exhibit='Africa Savanna',
         name='Outdoor' ),
      ViewingSpotReference(
         species='African Penguin',
         exhibit='Africa Savanna',
         name='Indoor' ),
   ],
)

RAINFOREST_LOOP = MasterRouteLoop(
   loop_id='african_rainforest_giraffe',
   name='African Rainforest',
   traversal=ONE_WAY_LOOP_TRAVERSAL,
   viewing_spots=[
      ViewingSpotReference(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         name='Indoor' ),
   ],
)

PENGUIN_OUTDOOR_LINK = GuardiansTalkAnimalRecord(
   talk_name='African Penguin',
   location='Africa Savanna',
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)


def Test_Resolve_TestLinkedOutdoorEnclosure_ExpectOutdoorIndex() -> None:
   assert GuardiansTalkLoopViewingSpotIndexResolver.resolve(
      AFRICA_SAVANNA_LOOP,
      talk_name='African Penguin',
      talk_location='Africa Savanna',
      linked_animals=[ PENGUIN_OUTDOOR_LINK ],
   ) == 1


def Test_Resolve_TestLinkedIndoorGorilla_ExpectIndoorIndex() -> None:
   assert GuardiansTalkLoopViewingSpotIndexResolver.resolve(
      RAINFOREST_LOOP,
      talk_name='Western Lowland Gorilla',
      talk_location='African Rainforest Pavilion',
      linked_animals=[
         GuardiansTalkAnimalRecord(
            talk_name='Western Lowland Gorilla',
            location='African Rainforest Pavilion',
            species='Western Lowland Gorilla',
            exhibit='African Rainforest Pavilion',
            enclosure_name='Indoor',
         ),
      ],
   ) == 0


def Test_Resolve_TestNullEnclosureLion_ExpectLionIndex() -> None:
   assert GuardiansTalkLoopViewingSpotIndexResolver.resolve(
      AFRICA_SAVANNA_LOOP,
      talk_name='African Lion',
      talk_location='Africa Savanna',
      linked_animals=[
         GuardiansTalkAnimalRecord(
            talk_name='African Lion',
            location='Africa Savanna',
            species='African Lion',
            exhibit='Africa Savanna',
         ),
      ],
   ) == 0


def Test_Resolve_TestLinkedEnclosureBeforeTalkNameMatch_ExpectOutdoorNotIndoor() -> None:
   index = GuardiansTalkLoopViewingSpotIndexResolver.resolve(
      AFRICA_SAVANNA_LOOP,
      talk_name='African Penguin',
      talk_location='Africa Savanna',
      linked_animals=[ PENGUIN_OUTDOOR_LINK ],
   )

   indoor_index = GuardiansTalkLoopViewingSpotIndexResolver.resolve(
      AFRICA_SAVANNA_LOOP,
      talk_name='African Penguin',
      talk_location='Africa Savanna',
      linked_animals=[
         GuardiansTalkAnimalRecord(
            talk_name='African Penguin',
            location='Africa Savanna',
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Indoor',
         ),
      ],
   )

   assert index == 1
   assert indoor_index == 2
   assert index != indoor_index
