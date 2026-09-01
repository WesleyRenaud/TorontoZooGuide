from __future__ import annotations

import sqlite3

import pytest

from api.guardians.data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from api.itinerary.scheduling.bulk.guardians_talk_animal_coverer import GuardiansTalkAnimalCoverer
from api.models.animal_diff import AnimalDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff


CARIBOU_TALK = 'Caribou'
CARIBOU_LINK = GuardiansTalkAnimalRecord(
   talk_name=CARIBOU_TALK,
   location='Tundra Trek',
   species='Caribou',
   exhibit='Tundra Trek',
)

CARIBOU_DIFF = AnimalDiff(
   species='Caribou',
   exhibit='Tundra Trek',
   old_likelihood=100,
   new_likelihood=100,
   covered_by_talk=True,
   start_time='3:00 PM',
   end_time='3:30 PM',
)

DELETED_CARIBOU_TALK = GuardiansTalkDiff(
   name=CARIBOU_TALK,
   is_deleted=True,
   start_time='3:00 PM',
   end_time='3:30 PM',
   location='Tundra Trek',
)


@pytest.fixture
def talk_coverer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_UncoverForUnavailableTalks_TestDeletedCaribouTalkCoveredAnimal_ExpectThreeMinuteWindow(
      talk_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ CARIBOU_LINK ] if talk_name == CARIBOU_TALK else [] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: 3 * 60 )

   animals = [
      AnimalDiff(
         species=CARIBOU_DIFF.species,
         exhibit=CARIBOU_DIFF.exhibit,
         old_likelihood=CARIBOU_DIFF.old_likelihood,
         new_likelihood=CARIBOU_DIFF.new_likelihood,
         covered_by_talk=CARIBOU_DIFF.covered_by_talk,
         start_time=CARIBOU_DIFF.start_time,
         end_time=CARIBOU_DIFF.end_time,
      ),
   ]

   result = GuardiansTalkAnimalCoverer.uncover_for_unavailable_talks(
      talk_coverer_conn,
      animals,
      [ DELETED_CARIBOU_TALK ],
   )

   assert result[ 0 ].covered_by_talk is False
   assert result[ 0 ].start_time == '3:00 PM'
   assert result[ 0 ].end_time == '3:03 PM'


def Test_UncoverForUnavailableTalks_TestDeletedTalkWithoutEnclosureDuration_ExpectScheduleCleared(
      talk_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ CARIBOU_LINK ] if talk_name == CARIBOU_TALK else [] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: None )

   animals = [
      AnimalDiff(
         species=CARIBOU_DIFF.species,
         exhibit=CARIBOU_DIFF.exhibit,
         old_likelihood=CARIBOU_DIFF.old_likelihood,
         new_likelihood=CARIBOU_DIFF.new_likelihood,
         covered_by_talk=CARIBOU_DIFF.covered_by_talk,
         start_time=CARIBOU_DIFF.start_time,
         end_time=CARIBOU_DIFF.end_time,
      ),
   ]

   result = GuardiansTalkAnimalCoverer.uncover_for_unavailable_talks(
      talk_coverer_conn,
      animals,
      [ DELETED_CARIBOU_TALK ],
   )

   assert result[ 0 ].covered_by_talk is False
   assert result[ 0 ].start_time is None
   assert result[ 0 ].end_time is None
