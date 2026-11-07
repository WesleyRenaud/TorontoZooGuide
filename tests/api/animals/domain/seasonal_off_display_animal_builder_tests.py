from __future__ import annotations

from datetime import date

from api.animals.data_access.animal_off_display_record import AnimalOffDisplayRecord
from api.animals.domain.seasonal_off_display_animal import SeasonalOffDisplayAnimal
from api.animals.domain.seasonal_off_display_animal_builder import SeasonalOffDisplayAnimalBuilder


STORK = 'Marabou Stork'


def Test_Build_TestRecords_ExpectAnimalNameStatusAndDates() -> None:
   animals = SeasonalOffDisplayAnimalBuilder.build(
      species=[ STORK, 'On Display' ],
      records=[
         AnimalOffDisplayRecord(
            species=STORK,
            is_off_display=True,
            start='2026-11-02',
            end='2026-11-30',
            off_for_season=True,
         ),
         AnimalOffDisplayRecord(
            species='Orphan',
            is_off_display=True,
            start='2026-10-01',
            end=None,
            off_for_season=True,
         ),
      ],
   )

   assert animals == [
      SeasonalOffDisplayAnimal(
         name=STORK,
         is_off_display=True,
         start=date( 2026, 11, 2 ),
         end=date( 2026, 11, 30 ),
         off_for_season=True,
      ),
      SeasonalOffDisplayAnimal(
         name='On Display',
         is_off_display=False,
         start=None,
         end=None,
         off_for_season=False,
      ),
      SeasonalOffDisplayAnimal(
         name='Orphan',
         is_off_display=True,
         start=date( 2026, 10, 1 ),
         end=None,
         off_for_season=True,
      ),
   ]


def Test_OffForSeasonOn_TestOpenEndedRange_ExpectOnlyCoveredDate() -> None:
   animal = SeasonalOffDisplayAnimal(
      name=STORK,
      is_off_display=True,
      start=date( 2026, 11, 2 ),
      end=None,
      off_for_season=True,
   )

   assert animal.off_for_season_on( date( 2026, 11, 2 ) )
   assert not animal.off_for_season_on( date( 2026, 11, 1 ) )


def Test_OffForSeasonOn_TestMissingStartAndPastEnd_ExpectNotOff() -> None:
   animal = SeasonalOffDisplayAnimal(
      name=STORK,
      is_off_display=True,
      start=None,
      end=date( 2026, 11, 1 ),
      off_for_season=True,
   )

   assert not animal.off_for_season_on( date( 2026, 11, 2 ) )


def Test_SpeciesName_TestCasefoldMatch_ExpectStoredName() -> None:
   animals = [ SeasonalOffDisplayAnimal(
      name=STORK,
      is_off_display=False,
      start=None,
      end=None,
      off_for_season=False,
   ) ]

   assert SeasonalOffDisplayAnimal.species_name( 'marabou stork', animals ) == STORK


def Test_SpeciesName_TestMissingName_ExpectGivenName() -> None:
   assert SeasonalOffDisplayAnimal.species_name( 'Unknown', [] ) == 'Unknown'
