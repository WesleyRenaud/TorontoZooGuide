from __future__ import annotations

from api.guardians.search.guardians_talks_matching_query_builder import GuardiansTalksMatchingQueryBuilder
from api.models.guardians_talk import GuardiansTalk


def Test_Build_TestMatchingQuery_ExpectMatchingTalkOnly() -> None:
   guardians_talks = [
      GuardiansTalk( 'Komodo Dragon', 'Australasia Pavilion', 0, 0 ),
      GuardiansTalk( 'Arctic Wolf', 'Tundra Trek', 0, 0 ),
   ]

   matches = GuardiansTalksMatchingQueryBuilder.build( guardians_talks, 'komodo' )

   assert [ talk.name for talk in matches ] == [ 'Komodo Dragon' ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingTalkOnly() -> None:
   guardians_talks = [
      GuardiansTalk( 'Komodo Dragon', 'Australasia Pavilion', 0, 0 ),
      GuardiansTalk( 'Arctic Wolf', 'Tundra Trek', 0, 0 ),
   ]

   matches = GuardiansTalksMatchingQueryBuilder.filter_matching_query(
      guardians_talks,
      'komodo' )

   assert [ talk.name for talk in matches ] == [ 'Komodo Dragon' ]


def Test_Build_TestEmptyQuery_ExpectAllTalks() -> None:
   guardians_talks = [
      GuardiansTalk( 'Komodo Dragon', 'Australasia Pavilion', 0, 0 ),
      GuardiansTalk( 'Arctic Wolf', 'Tundra Trek', 0, 0 ),
   ]

   matches = GuardiansTalksMatchingQueryBuilder.build( guardians_talks, '' )

   assert [ talk.name for talk in matches ] == [
      'Komodo Dragon',
      'Arctic Wolf',
   ]
