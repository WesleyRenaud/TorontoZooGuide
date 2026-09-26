from __future__ import annotations

from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.models.animal_diff import AnimalDiff
from api.shared.value_conversion import ValueConversion


def Test_ViewingSpotKey_TestEnclosureName_ExpectNormalizedTuple() -> None:
   diff = AnimalDiff(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=80,
      new_likelihood=60,
      enclosure_name='Indoor' )
   key = SpeciesExhibitKey.from_values( diff.species, diff.exhibit )

   result = diff.viewing_spot_key()

   assert result == (
      key.species,
      key.exhibit,
      ValueConversion.as_nullable_string( diff.enclosure_name ) )


def Test_ToDict_TestFields_ExpectFrontendShape() -> None:
   diff = AnimalDiff(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=80,
      new_likelihood=60,
      enclosure_name='Indoor',
      is_added=True,
      covered_by_talk=False,
      start_time='10:00 AM',
      end_time='10:30 AM' )

   result = diff.to_dict()

   assert result[ 'species' ] == diff.species
   assert result[ 'exhibit' ] == diff.exhibit
   assert result[ 'enclosure_name' ] == diff.enclosure_name
   assert result[ 'old_likelihood' ] == diff.old_likelihood
   assert result[ 'new_likelihood' ] == diff.new_likelihood
   assert result[ 'is_added' ] is diff.is_added
   assert result[ 'covered_by_talk' ] is diff.covered_by_talk
   assert result[ 'added_by_transportation' ] is diff.added_by_transportation
   assert result[ 'start_time' ] == diff.start_time
   assert result[ 'end_time' ] == diff.end_time
