from __future__ import annotations

import pytest

from api.attractions.itinerary.itinerary_attractions_builder import ItineraryAttractionsBuilder
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from api.models.attraction import Attraction


CAROUSEL = 'Conservation Carousel'
GREENHOUSE = 'Greenhouse'


def _attraction( name: str ) -> Attraction:
   return Attraction(
      name=name,
      free_with_admission=True )


def _saved_attraction(
      *,
      attraction: str,
      old_likelihood: int | None = None,
      start_time: str | None = None,
      end_time: str | None = None ) -> ItineraryAttractionRecord:
   return ItineraryAttractionRecord(
      attraction=attraction,
      old_likelihood=old_likelihood,
      new_likelihood=old_likelihood,
      start_time=start_time,
      end_time=end_time )


def Test_Build_TestEmptyInputs_ExpectEmpty() -> None:
   assert ItineraryAttractionsBuilder.build( [], [] ) == []


def Test_Build_TestFiltersSavedAttractions_ExpectOnlyMatching() -> None:
   attractions = [
      _attraction( CAROUSEL ),
      _attraction( GREENHOUSE ),
      _attraction( 'Tundra Air' ),
   ]
   saved_attractions = [
      _saved_attraction( attraction=CAROUSEL ),
      _saved_attraction( attraction=GREENHOUSE ),
   ]

   result = ItineraryAttractionsBuilder.build( attractions, saved_attractions )

   assert { attraction.name for attraction in result } == { CAROUSEL, GREENHOUSE }


def Test_Build_TestSortsByName_ExpectCaseInsensitiveOrder() -> None:
   attractions = [
      _attraction( GREENHOUSE ),
      _attraction( CAROUSEL ),
   ]
   saved_attractions = [
      _saved_attraction( attraction=GREENHOUSE ),
      _saved_attraction( attraction=CAROUSEL ),
   ]

   result = ItineraryAttractionsBuilder.build( attractions, saved_attractions )

   assert [ attraction.name for attraction in result ] == [ CAROUSEL, GREENHOUSE ]


def Test_Build_TestMissingSavedLookup_ExpectSkipsScheduleApplication(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   build_results = iter( [
      'carousel-key',
      'carousel-key',
      'carousel-key',
      'missing-key',
   ] )

   monkeypatch.setattr(
      ItineraryNameKeyBuilder,
      'build',
      lambda _name: next( build_results ) )
   attractions = [ _attraction( CAROUSEL ) ]
   saved_attractions = [
      _saved_attraction( attraction=CAROUSEL ),
   ]

   result = ItineraryAttractionsBuilder.build( attractions, saved_attractions )

   assert len( result ) == 1
   assert result[ 0 ].old_likelihood is None
   assert result[ 0 ].start_time is None
   assert result[ 0 ].end_time is None


def Test_Build_TestAppliesSavedSchedule_ExpectOldLikelihoodAndTimes() -> None:
   attractions = [ _attraction( CAROUSEL ) ]
   saved_attractions = [
      _saved_attraction(
         attraction=CAROUSEL,
         old_likelihood=90,
         start_time='11:00 AM',
         end_time='11:15 AM' ),
   ]

   result = ItineraryAttractionsBuilder.build( attractions, saved_attractions )

   carousel = result[ 0 ]
   assert carousel.old_likelihood == 90
   assert carousel.start_time == '11:00 AM'
   assert carousel.end_time == '11:15 AM'
