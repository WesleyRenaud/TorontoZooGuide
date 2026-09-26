from __future__ import annotations

from api.guardians.search.guardians_talks_matching_query_builder import GuardiansTalksMatchingQueryBuilder
from api.models.guardians_talk import GuardiansTalk


def Test_Build_TestMatchingQuery_ExpectMatchingTalkOnly() -> None:
   komodo_dragon = GuardiansTalk( 'Komodo Dragon', 'Australasia Pavilion', 0, 0 )
   arctic_wolf = GuardiansTalk( 'Arctic Wolf', 'Tundra Trek', 0, 0 )
   guardians_talks = [ komodo_dragon, arctic_wolf ]
   query = 'komodo'

   matches = GuardiansTalksMatchingQueryBuilder.build( guardians_talks, query )

   assert [ talk.name for talk in matches ] == [ komodo_dragon.name ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingTalkOnly() -> None:
   komodo_dragon = GuardiansTalk( 'Komodo Dragon', 'Australasia Pavilion', 0, 0 )
   arctic_wolf = GuardiansTalk( 'Arctic Wolf', 'Tundra Trek', 0, 0 )
   guardians_talks = [ komodo_dragon, arctic_wolf ]
   query = 'komodo'

   matches = GuardiansTalksMatchingQueryBuilder.filter_matching_query(
      guardians_talks,
      query )

   assert [ talk.name for talk in matches ] == [ komodo_dragon.name ]


def Test_Build_TestEmptyQuery_ExpectAllTalks() -> None:
   komodo_dragon = GuardiansTalk( 'Komodo Dragon', 'Australasia Pavilion', 0, 0 )
   arctic_wolf = GuardiansTalk( 'Arctic Wolf', 'Tundra Trek', 0, 0 )
   guardians_talks = [ komodo_dragon, arctic_wolf ]
   query = ''

   matches = GuardiansTalksMatchingQueryBuilder.build( guardians_talks, query )

   assert [ talk.name for talk in matches ] == [
      komodo_dragon.name,
      arctic_wolf.name,
   ]
