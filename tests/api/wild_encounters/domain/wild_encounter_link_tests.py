from __future__ import annotations

from api.wild_encounters.domain.wild_encounter_link import WildEncounterLink


GIRAFFE = 'Giraffe'
LINK = 'https://example.test/giraffe'


def Test_StoredName_TestCasefoldMatch_ExpectStoredName() -> None:
   encounter = WildEncounterLink( name=GIRAFFE, link=LINK )

   assert WildEncounterLink.stored_name( 'giraffe', [ encounter ] ) == GIRAFFE


def Test_StoredName_TestMissingName_ExpectGivenName() -> None:
   assert WildEncounterLink.stored_name( GIRAFFE, [] ) == GIRAFFE


def Test_BookingLink_TestStoredName_ExpectLink() -> None:
   encounter = WildEncounterLink( name=GIRAFFE, link=LINK )

   assert WildEncounterLink.booking_link( GIRAFFE, [ encounter ] ) == LINK
