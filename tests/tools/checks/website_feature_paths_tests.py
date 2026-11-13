from __future__ import annotations

from tools.checks.website_feature_paths import WebsiteFeaturePaths


HOME = """
<div class="mySlides"><a href="/maple">Maple</a></div>
<div class="mySlides"><a href="https://example.com/no">No</a></div>
<div class="mySlides"><a href="/fall?utm_source=events">Fall</a></div>
<article class="card-slider-item"><a href="https://www.torontozoo.com/glowinthewild">Glow</a></article>
<article class="card-slider-item"><a href="/animals">Animals</a></article>
"""

ANIMALS = """
<div class="c1280 iflexaround pgbut custom scrolling-title">
<a href="/wombat">Wombat</a>
<a href="/maple">Maple</a>
</div>
<a href="/alerts">Alerts</a>
<div class="pgbut"><a href="/animals/africa">Africa</a></div>
"""


def Test_FeaturePaths_TestSlidesCardsAndCustomRow_ExpectStoryPages() -> None:
   assert WebsiteFeaturePaths.feature_paths( HOME, ANIMALS ) == [
      'maple',
      'fall',
      'glowinthewild',
      'wombat',
   ]
