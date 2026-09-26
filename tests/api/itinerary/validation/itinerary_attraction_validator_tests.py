from __future__ import annotations

from datetime import date

import pytest

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.validation.itinerary_attraction_validator import ItineraryAttractionValidator


VISIT_DATE = date( 2026, 6, 15 )
CAROUSEL = 'Conservation Carousel'
GREENHOUSE = 'Greenhouse'
CAROUSEL_LIKELIHOOD = 0
GREENHOUSE_LIKELIHOOD = 100


@pytest.fixture
def stub_attraction_likelihoods( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attraction_likelihood_for_visit_date',
      lambda *, visit_date, attraction_name: {
         CAROUSEL: CAROUSEL_LIKELIHOOD,
         GREENHOUSE: GREENHOUSE_LIKELIHOOD,
      }.get( attraction_name, 0 ) )


def Test_Validate_TestClosedAndOpenAttractions_ExpectLikelihoods(
      stub_attraction_likelihoods: None ) -> None:
   attractions = [ CAROUSEL, GREENHOUSE ]
   arrival_time = '09:30'
   departure_time = '17:00'
   old_visit_date = '2026-06-15'

   result = ItineraryAttractionValidator.validate(
      AttractionCoordinator,
      attractions=attractions,
      new_visit_date=VISIT_DATE,
      arrival_time=arrival_time,
      departure_time=departure_time,
      old_visit_date=old_visit_date )

   assert [
      ( diff.name, diff.new_likelihood )
      for diff in result
      if diff.name == GREENHOUSE
   ] == [ ( GREENHOUSE, GREENHOUSE_LIKELIHOOD ) ]
   assert [
      ( diff.name, diff.new_likelihood )
      for diff in result
      if diff.name == CAROUSEL
   ] == [ ( CAROUSEL, CAROUSEL_LIKELIHOOD ) ]


def Test_Validate_TestSingleClosedAttraction_ExpectZeroLikelihood(
      stub_attraction_likelihoods: None ) -> None:
   attractions = [ CAROUSEL ]
   arrival_time = '09:30'
   departure_time = '17:00'
   old_visit_date = '2026-06-15'

   result = ItineraryAttractionValidator.validate(
      AttractionCoordinator,
      attractions=attractions,
      new_visit_date=VISIT_DATE,
      arrival_time=arrival_time,
      departure_time=departure_time,
      old_visit_date=old_visit_date )

   assert [
      ( diff.name, diff.new_likelihood )
      for diff in result
   ] == [ ( CAROUSEL, CAROUSEL_LIKELIHOOD ) ]
