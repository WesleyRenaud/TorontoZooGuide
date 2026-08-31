from __future__ import annotations

from datetime import date

import pytest

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.validation.itinerary_attraction_validator import ItineraryAttractionValidator


VISIT_DATE = date( 2026, 6, 15 )


@pytest.fixture
def stub_attraction_likelihoods( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attraction_likelihood_for_visit_date',
      lambda *, visit_date, attraction_name: {
         'Conservation Carousel': 0,
         'Greenhouse': 100,
      }.get( attraction_name, 0 ) )


def Test_Validate_TestClosedAndOpenAttractions_ExpectLikelihoods(
      stub_attraction_likelihoods: None ) -> None:
   result = ItineraryAttractionValidator.validate(
      AttractionCoordinator,
      attractions=[ 'Conservation Carousel', 'Greenhouse' ],
      new_visit_date=VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      old_visit_date='2026-06-15' )

   assert [
      ( diff.name, diff.new_likelihood )
      for diff in result
      if diff.name == 'Greenhouse'
   ] == [ ( 'Greenhouse', 100 ) ]
   assert [
      ( diff.name, diff.new_likelihood )
      for diff in result
      if diff.name == 'Conservation Carousel'
   ] == [ ( 'Conservation Carousel', 0 ) ]


def Test_Validate_TestSingleClosedAttraction_ExpectZeroLikelihood(
      stub_attraction_likelihoods: None ) -> None:
   result = ItineraryAttractionValidator.validate(
      AttractionCoordinator,
      attractions=[ 'Conservation Carousel' ],
      new_visit_date=VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      old_visit_date='2026-06-15' )

   assert [
      ( diff.name, diff.new_likelihood )
      for diff in result
   ] == [ ( 'Conservation Carousel', 0 ) ]
