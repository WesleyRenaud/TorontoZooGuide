from __future__ import annotations

from api.animals.domain.indoor_outdoor_viewing_visibility import apply_indoor_outdoor_viewing_visibility
from api.animals.domain.indoor_outdoor_viewing_visibility import should_exclude_indoor_viewing_spot
from api.models import Animal


def _animal(
      *,
      species: str = 'Masai Giraffe',
      exhibit: str = 'Africa Savanna',
      enclosure_type: str,
      likelihood: int,
      always_include_indoor_viewing: bool | None = None ) -> Animal:
   return Animal(
      species=species,
      exhibit=exhibit,
      enclosure_type=enclosure_type,
      enclosure_name=None,
      likelihood=likelihood,
      always_include_indoor_viewing=always_include_indoor_viewing )


def test_should_exclude_indoor_viewing_spot_when_flag_false_and_outdoor_likely() -> None:
   indoor = _animal(
      enclosure_type='Indoor',
      likelihood=100,
      always_include_indoor_viewing=False )

   assert should_exclude_indoor_viewing_spot(
      indoor,
      outdoor_likelihood=50 )
   assert should_exclude_indoor_viewing_spot(
      indoor,
      outdoor_likelihood=80 )
   assert not should_exclude_indoor_viewing_spot(
      indoor,
      outdoor_likelihood=49 )


def test_should_not_exclude_indoor_when_flag_true_or_null() -> None:
   indoor_true = _animal(
      enclosure_type='Indoor',
      likelihood=100,
      always_include_indoor_viewing=True )
   indoor_null = _animal(
      enclosure_type='Indoor',
      likelihood=100,
      always_include_indoor_viewing=None )

   assert not should_exclude_indoor_viewing_spot(
      indoor_true,
      outdoor_likelihood=100 )
   assert not should_exclude_indoor_viewing_spot(
      indoor_null,
      outdoor_likelihood=100 )


def test_apply_indoor_outdoor_viewing_visibility_excludes_indoor_for_exclusive_species() -> None:
   animals = [
      _animal( enclosure_type='Outdoor', likelihood=100 ),
      _animal(
         enclosure_type='Indoor',
         likelihood=100,
         always_include_indoor_viewing=False ),
   ]

   visible = apply_indoor_outdoor_viewing_visibility( animals )

   assert [ animal.enclosure_type for animal in visible ] == [ 'Outdoor' ]


def test_apply_indoor_outdoor_viewing_visibility_keeps_both_when_flag_true() -> None:
   animals = [
      _animal(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         enclosure_type='Outdoor',
         likelihood=100,
         always_include_indoor_viewing=True ),
      _animal(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         enclosure_type='Indoor',
         likelihood=100,
         always_include_indoor_viewing=True ),
   ]

   visible = apply_indoor_outdoor_viewing_visibility( animals )

   assert { animal.enclosure_type for animal in visible } == { 'Outdoor', 'Indoor' }
