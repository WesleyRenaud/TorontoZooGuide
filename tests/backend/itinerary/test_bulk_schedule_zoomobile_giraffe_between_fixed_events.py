from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry
from itinerary.support import itinerary_animals_for_exhibits
from itinerary.support import wild_encounter_key
from wild_encounter_schedule_support import wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

HYENA_TALK = 'Spotted Hyena'
TINY_TOUR = 'The Tiny Tour'
VISIT_DATE = '2026-07-11'


def test_bulk_schedule_packs_zoomobile_after_tiny_tour_and_giraffe_after_warthog(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 7, 11 ) )

   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=HYENA_TALK,
      location='Africa Savanna',
      start_date='2026-07-01',
      end_date='2026-07-31',
      schedule_rows=wire_schedule_rows(
         '14:00',
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ),
      message=None,
   )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=TINY_TOUR,
      start_date='2026-07-01',
      end_date='2026-07-31',
      schedule_rows=wire_schedule_rows(
         '11:00',
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ),
      message=None,
   )

   save = ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      arrival_time='09:00',
      departure_time='17:00',
      animals=itinerary_animals_for_exhibits(
         [ 'Africa Savanna' ],
         visit_date=VISIT_DATE ),
      attractions=[ 'Zoomobile' ],
      guardians_talks=[
         guardians_talk_save_entry( HYENA_TALK, start_time='14:00' ),
      ],
      wild_encounters=[
         wild_encounter_key( TINY_TOUR, start_time='11:00' ),
      ],
      selected_exhibits=[ 'Africa Savanna' ],
      confirming_early_admission=True,
   )

   assert save.success

   result = ItineraryCoordinator.bulk_schedule_animals(
      confirming_fixed_time_item_long_wait=True )

   assert result.success
   assert result.itinerary is not None

   zoomobile = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == 'Zoomobile' )
   giraffe = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Masai Giraffe' and animal.start_time is not None )
   warthog = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Warthog' and animal.start_time is not None )
   tiny_tour = next(
      encounter
      for encounter in result.itinerary.wild_encounters
      if encounter.name == TINY_TOUR )
   hyena_talk = next(
      talk
      for talk in result.itinerary.guardians_talks
      if talk.name == HYENA_TALK )

   assert zoomobile.start_time is not None
   assert zoomobile.end_time is not None
   assert giraffe.start_time is not None
   assert warthog.end_time is not None
   assert tiny_tour.end_time is not None
   assert hyena_talk.start_time is not None

   zoomobile_start = DateValues.time_value_in_seconds( zoomobile.start_time )
   zoomobile_end = DateValues.time_value_in_seconds( zoomobile.end_time )
   giraffe_start = DateValues.time_value_in_seconds( giraffe.start_time )
   warthog_end = DateValues.time_value_in_seconds( warthog.end_time )
   tiny_tour_end = DateValues.time_value_in_seconds( tiny_tour.end_time )
   hyena_talk_start = DateValues.time_value_in_seconds( hyena_talk.start_time )

   assert zoomobile_start is not None
   assert zoomobile_end is not None
   assert giraffe_start is not None
   assert warthog_end is not None
   assert tiny_tour_end is not None
   assert hyena_talk_start is not None

   assert zoomobile_start >= tiny_tour_end
   assert zoomobile_end <= hyena_talk_start
   assert warthog_end <= giraffe_start
