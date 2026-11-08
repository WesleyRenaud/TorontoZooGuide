from tools.checks.website_temporarily_off_display_animal import WebsiteTemporarilyOffDisplayAnimal


def Test_FromPage_TestTemporarilyNotViewable_ExpectAnimal() -> None:
   page = (
      '<div class="atitle scrolling-title" id="Indo-Malaya">'
      '<a href="/animals/Sumatran%20Orangutan">'
      '<span class="line2 status notviewable">Temporarily Not Viewable</span>'
      '</a>'
      '<a href="/animals/Marabou%20Stork">'
      '<span class="line2 status sseason">Off for the Season</span>'
      '</a>'
      '</div>'
   )

   animals = WebsiteTemporarilyOffDisplayAnimal.from_page( page )

   assert [ ( animal.section, animal.name ) for animal in animals ] == [
      ( 'Indo-Malaya', 'Sumatran Orangutan' ),
   ]
