from __future__ import annotations

import pytest

from tools.checks.website_closure import WebsiteClosure


PAGE = """
<h2 id="notices">Notices</h2>
<div class="box"><p><strong>Please note that some of our outdoor animals may not be viewable, as they have access to climate-controlled, behind-the-scenes habitats based on their seasonal needs.</strong></p></div>
<div class="box"><p><strong>Outdoor water fountains are closed for the season.</strong></p></div>
<div class="box"><p><strong>The Kids Zoo is closed for the winter season.</strong></p></div>
<div class="box"><details><summary><strong>Indo-Malaya Pavilion Construction</strong><br>expand for details</summary><p>The Sumatran orangutan indoor habitat is closed due to construction.</p></details></div>
<div class="box"><p><strong>The Mayan Temple Ruins will close early at 4:00pm.</strong></p></div>
<div class="box"><p><strong>Your Toronto Zoo will open late at 11:00am.</strong></p></div>
<div class="box"><p><strong>Washrooms will be unavailable on weekdays.</strong></p></div>
<h2 id="animals">Animals</h2>
"""


def Test_Closures_TestNotices_ExpectPlaceShutdownsOnly() -> None:
   closures = WebsiteClosure.closures( PAGE )
   titles = [ closure.title for closure in closures ]

   assert titles == [
      'Indo-Malaya Pavilion Construction',
      'The Mayan Temple Ruins will close early at 4:00pm.',
   ]


def Test_Closures_TestDetailsBody_ExpectBodyWithoutSummary() -> None:
   closure = WebsiteClosure.closures( PAGE )[ 0 ]

   assert closure.description == (
      'The Sumatran orangutan indoor habitat is closed due to construction.'
   )
   assert 'expand for details' not in closure.description


def Test_NoticesSection_TestMissingHeading_ExpectReadError() -> None:
   with pytest.raises( RuntimeError, match='Could not read the alerts page.' ):
      WebsiteClosure.notices( '<p>No notices heading</p>' )
