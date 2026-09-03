from __future__ import annotations

from api.animals.domain.indoor_outdoor_viewing_visibility_builder import IndoorOutdoorViewingVisibilityBuilder
from api.animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from api.models.animal import Animal


ANIMAL_SPECIES = 'Masai Giraffe'
ANIMAL_EXHIBIT = 'Africa Savanna'
GORILLA_SPECIES = 'Western Lowland Gorilla'
GORILLA_EXHIBIT = 'African Rainforest Pavilion'
OUTDOOR_ENCLOSURE_TYPE = 'Outdoor'
INDOOR_ENCLOSURE_TYPE = 'Indoor'
EXISTING_ALERT_MESSAGE = 'Existing alert.'
INDOOR_ALERT_MESSAGE = (
   'If you do not see the Masai Giraffe inside, '
   'then check their outdoor habitat.' )
OUTDOOR_ALERT_MESSAGE = (
   'If you do not see the Masai Giraffe outside, '
   'then check their indoor habitat.' )


def _animal(
      *,
      species: str = ANIMAL_SPECIES,
      exhibit: str = ANIMAL_EXHIBIT,
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


def Test_EffectiveViewingLikelihood_TestSingleHabitatOutdoor_ExpectOutdoorLikelihood() -> None:
   outdoor = _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=30 )

   assert IndoorOutdoorViewingVisibilityBuilder.effective_viewing_likelihood(
      outdoor,
      outdoor_likelihood=30,
      single_habitat=True ) == 30


def Test_EffectiveViewingLikelihood_TestSingleHabitatIndoor_ExpectComplementaryLikelihood() -> None:
   indoor = _animal( enclosure_type=INDOOR_ENCLOSURE_TYPE, likelihood=100 )

   assert IndoorOutdoorViewingVisibilityBuilder.effective_viewing_likelihood(
      indoor,
      outdoor_likelihood=30,
      single_habitat=True ) == 70


def Test_EffectiveViewingLikelihood_TestMultiHabitatIndoor_ExpectIndoorLikelihood() -> None:
   indoor = _animal( enclosure_type=INDOOR_ENCLOSURE_TYPE, likelihood=100 )

   assert IndoorOutdoorViewingVisibilityBuilder.effective_viewing_likelihood(
      indoor,
      outdoor_likelihood=30,
      single_habitat=False ) == 100


def Test_PreferredSingleHabitatViewingSpotBySpeciesExhibit_TestHigherIndoorLikelihood_ExpectIndoor() -> None:
   animals = [
      _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=30 ),
      _animal(
         enclosure_type=INDOOR_ENCLOSURE_TYPE,
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   assert _preferred( animals, outdoor_likelihood=30 ).enclosure_type == INDOOR_ENCLOSURE_TYPE


def Test_PreferredSingleHabitatViewingSpotBySpeciesExhibit_TestHigherOutdoorLikelihood_ExpectOutdoor() -> None:
   animals = [
      _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=30 ),
      _animal(
         enclosure_type=INDOOR_ENCLOSURE_TYPE,
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   assert _preferred( animals, outdoor_likelihood=80 ).enclosure_type == OUTDOOR_ENCLOSURE_TYPE


def Test_PreferredSingleHabitatViewingSpotBySpeciesExhibit_TestTiedLikelihood_ExpectOutdoor() -> None:
   animals = [
      _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=50 ),
      _animal(
         enclosure_type=INDOOR_ENCLOSURE_TYPE,
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   assert _preferred( animals, outdoor_likelihood=50 ).enclosure_type == OUTDOOR_ENCLOSURE_TYPE


def Test_Apply_TestExclusiveOutdoorSpecies_ExpectOutdoorOnly() -> None:
   animals = [
      _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=100 ),
      _animal(
         enclosure_type=INDOOR_ENCLOSURE_TYPE,
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert [ animal.enclosure_type for animal in visible ] == [ OUTDOOR_ENCLOSURE_TYPE ]
   assert visible[ 0 ].likelihood == 100


def Test_Apply_TestExclusiveIndoorSpecies_ExpectIndoorOnly() -> None:
   animals = [
      _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=30 ),
      _animal(
         enclosure_type=INDOOR_ENCLOSURE_TYPE,
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert [ animal.enclosure_type for animal in visible ] == [ INDOOR_ENCLOSURE_TYPE ]
   assert visible[ 0 ].likelihood == 100


def Test_SingleHabitatAlternateEnclosureViewingAlertMessage_TestOutdoorAnimal_ExpectIndoorAlternateMessage() -> None:
   outdoor = _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=80 )

   assert IndoorOutdoorViewingVisibilityBuilder.single_habitat_alternate_enclosure_viewing_alert_message(
      outdoor ) == OUTDOOR_ALERT_MESSAGE


def Test_SingleHabitatAlternateEnclosureViewingAlertMessage_TestIndoorAnimal_ExpectOutdoorAlternateMessage() -> None:
   indoor = _animal( enclosure_type=INDOOR_ENCLOSURE_TYPE, likelihood=70 )

   assert IndoorOutdoorViewingVisibilityBuilder.single_habitat_alternate_enclosure_viewing_alert_message(
      indoor ) == INDOOR_ALERT_MESSAGE


def Test_ApplySingleHabitatAlternateEnclosureViewingAlert_TestFullLikelihood_ExpectNoAlert() -> None:
   outdoor = _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=100 )

   IndoorOutdoorViewingVisibilityBuilder.apply_single_habitat_alternate_enclosure_viewing_alert(
      outdoor,
      outdoor_likelihood=100 )

   assert outdoor.has_viewing_alert is False
   assert outdoor.viewing_alert_messages == []


def Test_ApplySingleHabitatAlternateEnclosureViewingAlert_TestIndoorAnimal_ExpectAlternateAlert() -> None:
   indoor = _animal( enclosure_type=INDOOR_ENCLOSURE_TYPE, likelihood=100 )

   IndoorOutdoorViewingVisibilityBuilder.apply_single_habitat_alternate_enclosure_viewing_alert(
      indoor,
      outdoor_likelihood=30 )

   assert indoor.has_viewing_alert is True
   assert indoor.viewing_alert_messages == [ INDOOR_ALERT_MESSAGE ]


def Test_ApplySingleHabitatAlternateEnclosureViewingAlert_TestExistingMessages_ExpectPreservedMessages() -> None:
   outdoor = _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=80 )
   outdoor.viewing_alert_messages = [ EXISTING_ALERT_MESSAGE ]

   IndoorOutdoorViewingVisibilityBuilder.apply_single_habitat_alternate_enclosure_viewing_alert(
      outdoor,
      outdoor_likelihood=80 )

   assert outdoor.has_viewing_alert is True
   assert outdoor.viewing_alert_messages == [
      EXISTING_ALERT_MESSAGE,
      OUTDOOR_ALERT_MESSAGE,
   ]


def Test_Apply_TestBelowFullLikelihood_ExpectAlternateEnclosureAlert() -> None:
   animals = [
      _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=30 ),
      _animal(
         enclosure_type=INDOOR_ENCLOSURE_TYPE,
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert len( visible ) == 1
   assert visible[ 0 ].enclosure_type == INDOOR_ENCLOSURE_TYPE
   assert visible[ 0 ].likelihood == 100
   assert visible[ 0 ].has_viewing_alert is True
   assert visible[ 0 ].viewing_alert_messages == [ INDOOR_ALERT_MESSAGE ]


def Test_Apply_TestFullLikelihood_ExpectNoAlert() -> None:
   animals = [
      _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=100 ),
      _animal(
         enclosure_type=INDOOR_ENCLOSURE_TYPE,
         likelihood=100,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert len( visible ) == 1
   assert visible[ 0 ].enclosure_type == OUTDOOR_ENCLOSURE_TYPE
   assert visible[ 0 ].has_viewing_alert is False
   assert visible[ 0 ].viewing_alert_messages == []


def Test_Apply_TestClosedExhibit_ExpectZeroLikelihoodRetained() -> None:
   animals = [
      _animal( enclosure_type=OUTDOOR_ENCLOSURE_TYPE, likelihood=0 ),
      _animal(
         enclosure_type=INDOOR_ENCLOSURE_TYPE,
         likelihood=0,
         include_all_viewing_spots=False ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert len( visible ) == 2
   assert all( animal.likelihood == 0 for animal in visible )


def Test_SingleHabitatAlternateEnclosureViewingAlertMessage_TestMissingEnclosureType_ExpectNone() -> None:
   animal = _animal( enclosure_type='', likelihood=80 )

   assert IndoorOutdoorViewingVisibilityBuilder.single_habitat_alternate_enclosure_viewing_alert_message(
      animal ) is None


def Test_ApplySingleHabitatAlternateEnclosureViewingAlert_TestMissingEnclosureType_ExpectNoAlert() -> None:
   animal = _animal( enclosure_type='', likelihood=80 )

   IndoorOutdoorViewingVisibilityBuilder.apply_single_habitat_alternate_enclosure_viewing_alert(
      animal,
      outdoor_likelihood=80 )

   assert animal.has_viewing_alert is False
   assert animal.viewing_alert_messages == []


def Test_Apply_TestIncludeAllViewingSpots_ExpectBothEnclosures() -> None:
   animals = [
      _animal(
         species=GORILLA_SPECIES,
         exhibit=GORILLA_EXHIBIT,
         enclosure_type=OUTDOOR_ENCLOSURE_TYPE,
         likelihood=100,
         include_all_viewing_spots=True ),
      _animal(
         species=GORILLA_SPECIES,
         exhibit=GORILLA_EXHIBIT,
         enclosure_type=INDOOR_ENCLOSURE_TYPE,
         likelihood=100,
         include_all_viewing_spots=True ),
   ]

   visible = IndoorOutdoorViewingVisibilityBuilder.apply( animals )

   assert { animal.enclosure_type for animal in visible } == {
      OUTDOOR_ENCLOSURE_TYPE,
      INDOOR_ENCLOSURE_TYPE,
   }
