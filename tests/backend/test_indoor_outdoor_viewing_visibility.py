from __future__ import annotations

from api.animals.domain.indoor_outdoor_viewing_visibility_builder import IndoorOutdoorViewingVisibilityBuilder
from api.animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from api.models import Animal


def _animal(
      *,
      species: str = 'Masai Giraffe',
      exhibit: str = 'Africa Savanna',
      enclosure_type: str,
      likelihood: int,
      include_all_viewing_spots: bool | None = None ) -> Animal:
   return Animal(
      species=species,
      exhibit=exhibit,
      enclosure_type=enclosure_type,
      enclosure_name=None,
      likelihood=likelihood,
      include_all_viewing_spots=include_all_viewing_spots )


def _preferred(
      animals: list[ Animal ],
      *,
      outdoor_likelihood: int ) -> Animal:
   single_habitat_keys = IndoorOutdoorViewingVisibilityBuilder.single_habitat_viewing_species_exhibit_keys( animals )
   key = SpeciesExhibitKeyBuilder.from_animal( animals[ 0 ] )
   outdoor_likelihood_by_species_exhibit = { key: outdoor_likelihood }

   return IndoorOutdoorViewingVisibilityBuilder.preferred_single_habitat_viewing_spot_by_species_exhibit(
      animals,
      outdoor_likelihood_by_species_exhibit=outdoor_likelihood_by_species_exhibit,
      single_habitat_species_exhibit_keys=single_habitat_keys )[ key ]


def test_effective_viewing_likelihood_uses_complementary_indoor_only_for_single_habitat() -> None:
   outdoor = _animal( enclosure_type='Outdoor', likelihood=30 )
   indoor = _animal( enclosure_type='Indoor', likelihood=100 )

   assert IndoorOutdoorViewingVisibilityBuilder.effective_viewing_likelihood(
      outdoor,
      outdoor_likelihood=30,
      single_habitat=True ) == 30
   assert IndoorOutdoorViewingVisibilityBuilder.effective_viewing_likelihood(
      indoor,
      outdoor_likelihood=30,
      single_habitat=True ) == 70
   assert IndoorOutdoorViewingVisibilityBuilder.effective_viewing_likelihood(
      indoor,
      outdoor_likelihood=30,
      single_habitat=False ) == 100


def test_preferred_single_habitat_viewing_spot_picks_highest_likelihood() -> None:
   animals = [
      _animal( enclosure_type='Outdoor', likelihood=30 ),
      _animal(
         enclosure_type='Indoor',
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   assert _preferred( animals, outdoor_likelihood=30 ).enclosure_type == 'Indoor'
   assert _preferred( animals, outdoor_likelihood=80 ).enclosure_type == 'Outdoor'


def test_preferred_single_habitat_viewing_spot_prefers_outdoor_on_tie() -> None:
   animals = [
      _animal( enclosure_type='Outdoor', likelihood=50 ),
      _animal(
         enclosure_type='Indoor',
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   assert _preferred( animals, outdoor_likelihood=50 ).enclosure_type == 'Outdoor'


def test_apply_indoor_outdoor_viewing_visibility_excludes_indoor_for_exclusive_species() -> None:
   animals = [
      _animal( enclosure_type='Outdoor', likelihood=100 ),
      _animal(
         enclosure_type='Indoor',
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert [ animal.enclosure_type for animal in visible ] == [ 'Outdoor' ]
   assert visible[ 0 ].likelihood == 100


def test_apply_indoor_outdoor_viewing_visibility_excludes_outdoor_for_exclusive_species() -> None:
   animals = [
      _animal( enclosure_type='Outdoor', likelihood=30 ),
      _animal(
         enclosure_type='Indoor',
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert [ animal.enclosure_type for animal in visible ] == [ 'Indoor' ]
   assert visible[ 0 ].likelihood == 100


def test_single_habitat_alternate_enclosure_viewing_alert_message() -> None:
   outdoor = _animal( enclosure_type='Outdoor', likelihood=80 )

   assert IndoorOutdoorViewingVisibilityBuilder.single_habitat_alternate_enclosure_viewing_alert_message( outdoor ) == (
      'If you do not see the Masai Giraffe outside, '
      'then check their indoor habitat.' )

   indoor = _animal( enclosure_type='Indoor', likelihood=70 )

   assert IndoorOutdoorViewingVisibilityBuilder.single_habitat_alternate_enclosure_viewing_alert_message( indoor ) == (
      'If you do not see the Masai Giraffe inside, '
      'then check their outdoor habitat.' )


def test_apply_single_habitat_alternate_enclosure_viewing_alert_skips_full_likelihood() -> None:
   outdoor = _animal( enclosure_type='Outdoor', likelihood=100 )

   IndoorOutdoorViewingVisibilityBuilder.apply_single_habitat_alternate_enclosure_viewing_alert(
      outdoor,
      outdoor_likelihood=100 )

   assert outdoor.has_viewing_alert is False
   assert outdoor.viewing_alert_messages == []


def test_apply_single_habitat_alternate_enclosure_viewing_alert_uses_effective_likelihood_for_indoor() -> None:
   indoor = _animal( enclosure_type='Indoor', likelihood=100 )

   IndoorOutdoorViewingVisibilityBuilder.apply_single_habitat_alternate_enclosure_viewing_alert(
      indoor,
      outdoor_likelihood=30 )

   assert indoor.has_viewing_alert is True
   assert indoor.viewing_alert_messages == [
      'If you do not see the Masai Giraffe inside, '
      'then check their outdoor habitat.',
   ]


def test_apply_single_habitat_alternate_enclosure_viewing_alert_preserves_existing_messages() -> None:
   outdoor = _animal( enclosure_type='Outdoor', likelihood=80 )
   outdoor.viewing_alert_messages = [ 'Existing alert.' ]

   IndoorOutdoorViewingVisibilityBuilder.apply_single_habitat_alternate_enclosure_viewing_alert(
      outdoor,
      outdoor_likelihood=80 )

   assert outdoor.has_viewing_alert is True
   assert outdoor.viewing_alert_messages == [
      'Existing alert.',
      'If you do not see the Masai Giraffe outside, '
      'then check their indoor habitat.',
   ]


def test_apply_indoor_outdoor_viewing_visibility_adds_alert_when_likelihood_below_100() -> None:
   animals = [
      _animal( enclosure_type='Outdoor', likelihood=30 ),
      _animal(
         enclosure_type='Indoor',
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert len( visible ) == 1
   assert visible[ 0 ].enclosure_type == 'Indoor'
   assert visible[ 0 ].likelihood == 100
   assert visible[ 0 ].has_viewing_alert is True
   assert visible[ 0 ].viewing_alert_messages == [
      'If you do not see the Masai Giraffe inside, '
      'then check their outdoor habitat.',
   ]


def test_apply_indoor_outdoor_viewing_visibility_skips_alert_at_full_likelihood() -> None:
   animals = [
      _animal( enclosure_type='Outdoor', likelihood=100 ),
      _animal(
         enclosure_type='Indoor',
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert len( visible ) == 1
   assert visible[ 0 ].enclosure_type == 'Outdoor'
   assert visible[ 0 ].has_viewing_alert is False
   assert visible[ 0 ].viewing_alert_messages == []


def test_apply_indoor_outdoor_viewing_visibility_keeps_zero_likelihood_when_exhibit_closed() -> None:
   animals = [
      _animal( enclosure_type='Outdoor', likelihood=0 ),
      _animal(
         enclosure_type='Indoor',
         likelihood=0,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert len( visible ) == 2
   assert all( animal.likelihood == 0 for animal in visible )


def test_apply_indoor_outdoor_viewing_visibility_keeps_both_when_flag_true() -> None:
   animals = [
      _animal(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         enclosure_type='Outdoor',
         likelihood=100,
         include_all_viewing_spots=True ),
      _animal(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         enclosure_type='Indoor',
         likelihood=100,
         include_all_viewing_spots=True ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert { animal.enclosure_type for animal in visible } == { 'Outdoor', 'Indoor' }
