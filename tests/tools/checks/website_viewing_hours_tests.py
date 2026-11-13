from __future__ import annotations

from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from tools.checks.website_viewing_hours import WebsiteViewingHours


HIPPO = 'Pygmy Hippopotamus'
PAVILION = 'African Rainforest Pavilion'
GORILLA = 'Western Lowland Gorilla'
GIRAFFE = 'Masai Giraffe'
SAVANNA = 'Africa Savanna'
OTTER = 'North American River Otter'
AMERICAS = 'Americas Pavilion'
HIPPO_SAVANNA = 'River Hippopotamus'

MAPLE = """
<div>Daily: 9:30am - 4:30pm</div>
<style>.banner { content: "Daily from 1:00am - 2:00am"; }</style>
<h1>Daily from 10:30am - 2:30pm *, come meet the newest addition in the African Rainforest Pavilion.</h1>
<p>The Western Lowland Gorilla and Ring-Tailed Lemur live nearby.</p>
<a href="https://www.torontozoo.com/animals/Pygmy hippopotamus">Learn More About Pygmy Hippopotamus</a>
"""


def _placement( species: str, exhibit: str ) -> AnimalSpeciesExhibit:
   return AnimalSpeciesExhibit( species=species, exhibit=exhibit )


def _hours(
      page_html: str,
      page_path: str,
      placements: list[ AnimalSpeciesExhibit ] ) -> list[ tuple[ str, str, str, str ] ]:
   return [
      ( item.species, item.exhibit, item.opens, item.closes )
      for item in WebsiteViewingHours.schedules( page_html, page_path, placements )
   ]


def Test_Schedules_TestDailyFromHeading_ExpectPavilionHours() -> None:
   placements = [
      _placement( HIPPO, PAVILION ),
      _placement( GORILLA, PAVILION ),
   ]

   assert _hours( MAPLE, 'maple', placements ) == [
      ( HIPPO, PAVILION, '10:30 AM', '2:30 PM' ),
   ]


def Test_Schedules_TestSeenDailyWithoutClock_ExpectNoHours() -> None:
   page = '<p>Zorig and family can be seen daily in their Eurasia Wilds habitat.</p>'
   placements = [ _placement( 'Bactrian Camel', 'Eurasia Wilds' ) ]

   assert _hours( page, 'camel', placements ) == []


def Test_Schedules_TestSpeciesPage_ExpectPathSpecies() -> None:
   page = '<h1>Daily from 10:00am - 1:00pm in the Americas Pavilion.</h1>'
   placements = [ _placement( OTTER, AMERICAS ) ]

   assert _hours( page, 'animals/North American River Otter', placements ) == [
      ( OTTER, AMERICAS, '10:00 AM', '1:00 PM' ),
   ]


def Test_Schedules_TestHoursWithoutExhibitName_ExpectNoHours() -> None:
   page = """
<h1>Daily from 11:00am - 1:00pm.</h1>
<a href="/animals/Masai%20giraffe">Learn More</a>
"""
   placements = [ _placement( GIRAFFE, SAVANNA ) ]

   assert _hours( page, 'giraffe', placements ) == []


def Test_Schedules_TestNamedHeadingWithoutLink_ExpectThatSpecies() -> None:
   page = '<h1>Daily from 11:00am - 1:00pm, meet the Masai Giraffe in the Africa Savanna.</h1>'
   placements = [ _placement( GIRAFFE, SAVANNA ) ]

   assert _hours( page, 'giraffe', placements ) == [
      ( GIRAFFE, SAVANNA, '11:00 AM', '1:00 PM' ),
   ]


def Test_Schedules_TestTwoExhibitsWithoutName_ExpectNoHours() -> None:
   page = """
<h1>Daily from 10:00am - 2:00pm.</h1>
<a href="/animals/River%20Hippopotamus">Learn More</a>
"""
   placements = [
      _placement( HIPPO_SAVANNA, SAVANNA ),
      _placement( HIPPO_SAVANNA, PAVILION ),
   ]

   assert _hours( page, 'hippo', placements ) == []
