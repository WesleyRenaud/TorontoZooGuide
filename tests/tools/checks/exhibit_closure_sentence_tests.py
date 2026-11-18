from __future__ import annotations

from tools.checks.exhibit_closure_sentence import ExhibitClosureSentence


NAMES = [
   'Africa Savanna',
   'African Rainforest Pavilion',
   'Americas Pavilion',
   'Canadian Domain',
   'Eurasia Wilds',
   'Indo-Malaya Outdoor',
   'Indo-Malaya Pavilion',
   'Tundra Trek',
]


def closed( sentence: str ) -> list[ str ]:
   return ExhibitClosureSentence.closed_names( sentence, NAMES )


def Test_ClosedNames_TestExhibitIsClosed_ExpectThatExhibit() -> None:
   assert closed(
      'The Canadian Domain is closed due to current weather conditions.',
   ) == [ 'Canadian Domain' ]


def Test_ClosedNames_TestEarlyClose_ExpectThatExhibit() -> None:
   assert closed(
      "The America's Pavilion will close at 4:15pm for maintenance until further notice.",
   ) == [ 'Americas Pavilion' ]


def Test_ClosedNames_TestNamedRange_ExpectThatExhibit() -> None:
   assert closed(
      'The Americas Pavilion will be closed from Monday, March 23rd until Friday, March 27th due to maintenance.',
   ) == [ 'Americas Pavilion' ]


def Test_ClosedNames_TestAreasNotAccessible_ExpectThatExhibit() -> None:
   assert closed(
      'The African penguins, Watusi, Hyenas, Red Panda, and Canadian Domain areas will not be visible or accessible.',
   ) == [ 'Canadian Domain' ]


def Test_ClosedNames_TestPathInsideExhibit_ExpectNothing() -> None:
   assert closed(
      'Tundra Trek: Caribou may not be visible and the path to the Caribou habitat may be closed for the entire day.',
   ) == []


def Test_ClosedNames_TestPathwayPortion_ExpectNothing() -> None:
   assert closed(
      'A portion of the Eurasia Wilds loop pathway between the former red panda habitat and the camels is closed due to construction.',
   ) == []


def Test_ClosedNames_TestBoardwalkBetweenExhibits_ExpectNothing() -> None:
   assert closed(
      'The boardwalk between Indo-Malaya and Africa is closed for some exciting changes.',
   ) == []


def Test_ClosedNames_TestWashroomAtExhibit_ExpectNothing() -> None:
   assert closed(
      'The washroom at the top of Canadian Domain Hill is closed due to construction.',
   ) == []


def Test_ClosedNames_TestClosedForTheSeason_ExpectNothing() -> None:
   assert closed( 'Canadian Domain is closed for the season.' ) == []
