from __future__ import annotations

from dataclasses import replace
from datetime import date

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...animals.search.animals_matching_query import species_exhibit_key
from ...animals.search.animals_matching_query import species_exhibit_key_from_values
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_animal_input import ItineraryAnimalInput
from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_animal_save_carryover import itinerary_animal_save_carryover
from ..data_access.itinerary_animal_save_carryover import ItineraryAnimalSaveCarryover
from ..data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ..data_access.itinerary_attraction_save_carryover import itinerary_attraction_save_carryover
from ..data_access.itinerary_event_record import ItineraryEventRecord
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.itinerary_transportation_input import ItineraryTransportationInput
from ..data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ..data_access.itinerary_transportation_save_carryover import itinerary_transportation_save_carryover
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ..domain.build_transportation_route_marker_sequences import build_transportation_route_marker_sequences
from ..domain.itinerary_visit_window import cleared_schedule_times_for_visit_window
from ..domain.itinerary_visit_window import schedule_time_occurs_outside_visit_window
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...guardians.itinerary.guardians_talk_itinerary_validation import validate_guardians_talks_for_itinerary
from ...models import Animal
from ...models import AnimalDiff
from ...models import AttractionDiff
from ...models import GuardiansTalkDiff
from ...models import TransportationDiff
from ...models import WildEncounterDiff
from ...models.itinerary_event import ItineraryEvent
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ..scheduling.bulk.attraction_covered_animals import uncover_animals_for_removed_attractions
from ..scheduling.bulk.guardians_talk_covered_animals import uncover_animals_for_unavailable_talks
from ..scheduling.extend_departure_for_activity import arrival_time_covering_schedule_starts
from ..scheduling.extend_departure_for_activity import departure_time_covering_schedule_ends
from .selected_exhibit_date_change_animals import apply_selected_exhibit_animals_on_date_change
from ...shared.enums import ItineraryEventType
from ...shared.value_conversion import ValueConversion
from ..transportation.expand_timed_transportation_legs import expand_timed_transportation_legs
from ..transportation.resolve_transportation_day_loop import fetch_transportation_day_loop
from ..transportation.resolve_transportation_day_loop import resolve_transportation_route_for_date
from ...types import Connection, DateKey, ScheduleTimeKey
from ..warnings.guardians_talk_unschedule_warning import new_guardians_talks_overlapping_saved_schedule
from ..warnings.wild_encounter_unschedule_warning import new_wild_encounters_overlapping_saved_schedule
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ...wild_encounters.itinerary.wild_encounter_itinerary_validation import validate_wild_encounters_for_itinerary


def _preferred_habitat_for_removed_animal(
      animal_coordinator: type[ AnimalCoordinator ],
      *,
      visit_date: date,
      visit_date_temp: float | None,
      removed: ItineraryAnimalSaveCarryover ) -> Animal | None:
   # Single-habitat visibility already leaves at most one preferred spot
   # (outdoor↔indoor). Reuse that as the replacement either direction.
   preferred_habitats = [
      animal
      for animal in animal_coordinator.get_animals_viewable_on_day(
         day=visit_date.day,
         month=visit_date.month,
         year=visit_date.year,
         temp=visit_date_temp,
         include_off_display_animals=True,
         threshold=0,
         exhibits_to_include=[ removed.exhibit ] )
      if (
         species_exhibit_key( animal )
         == species_exhibit_key_from_values( removed.species, removed.exhibit ) )
   ]

   if len( preferred_habitats ) != 1:
      return None

   return preferred_habitats[ 0 ]


def _animal_diff_from_carryover(
      carryover: ItineraryAnimalSaveCarryover,
      *,
      enclosure_name: str | None,
      new_likelihood: int | None,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> AnimalDiff:
   return AnimalDiff(
      species=carryover.species,
      exhibit=carryover.exhibit,
      enclosure_name=enclosure_name,
      old_likelihood=carryover.old_likelihood,
      new_likelihood=new_likelihood,
      is_added=carryover.is_added,
      covered_by_talk=carryover.covered_by_talk,
      start_time=start_time,
      end_time=end_time,
   )


def validate_itinerary_animals(
      animal_coordinator: type[ AnimalCoordinator ],
      animals: list[ ItineraryAnimalInput ],
      new_visit_date: date,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey,
      new_visit_date_temp: float | None = None,
      old_visit_date: DateKey | None = None,
      saved_animal_rows: list[ ItineraryAnimalRecord ] | None = None,
      visit_date_is_changing: bool = False ) -> list[ AnimalDiff ]:
   diffs: list[ AnimalDiff ] = []
   removed_habitats: list[ tuple[
      ItineraryAnimalSaveCarryover,
      ScheduleTimeKey,
      ScheduleTimeKey,
   ] ] = []

   for animal in animals:
      carryover = itinerary_animal_save_carryover(
         saved_animal_rows,
         animal,
         old_visit_date=old_visit_date )
      start_time, end_time = (
         ( carryover.start_time, carryover.end_time )
         if visit_date_is_changing
         else cleared_schedule_times_for_visit_window(
            carryover.start_time,
            carryover.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ) )

      saved_animals = animal_coordinator.get_animals_for_saved_itinerary(
         day=new_visit_date.day,
         month=new_visit_date.month,
         year=new_visit_date.year,
         temp=new_visit_date_temp,
         saved_animals=[
            ItineraryAnimalRecord(
               species=carryover.species,
               exhibit=carryover.exhibit,
               enclosure_name=carryover.enclosure_name,
               old_likelihood=None,
               new_likelihood=None ) ],
      )

      if not saved_animals:
         # Habitat is not viewable on this day. Pool removals so they can be
         # replaced with the preferred single-habitat spot below.
         removed_habitats.append( ( carryover, start_time, end_time ) )
         continue

      diffs.append(
         _animal_diff_from_carryover(
            carryover,
            enclosure_name=carryover.enclosure_name,
            new_likelihood=max(
               ( a.likelihood or 0 ) for a in saved_animals ),
            start_time=start_time,
            end_time=end_time ) )

   for carryover, start_time, end_time in removed_habitats:
      preferred = _preferred_habitat_for_removed_animal(
         animal_coordinator,
         visit_date=new_visit_date,
         visit_date_temp=new_visit_date_temp,
         removed=carryover )

      if preferred is None:
         diffs.append(
            _animal_diff_from_carryover(
               carryover,
               enclosure_name=carryover.enclosure_name,
               new_likelihood=None,
               start_time=start_time,
               end_time=end_time ) )
         continue

      enclosure_name = ValueConversion.as_nullable_string(
         preferred.enclosure_name )
      already_present = any(
         diff.species == carryover.species
         and diff.exhibit == carryover.exhibit
         and diff.enclosure_name == enclosure_name
         for diff in diffs )

      if already_present:
         continue

      diffs.append(
         _animal_diff_from_carryover(
            carryover,
            enclosure_name=enclosure_name,
            new_likelihood=preferred.likelihood or 0,
            start_time=start_time,
            end_time=end_time ) )

   return diffs



def validate_itinerary_attractions(
      attraction_coordinator: type[ AttractionCoordinator ],
      attractions: list[ str ],
      new_visit_date: date,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey,
      old_visit_date: DateKey | None = None,
      saved_attraction_rows: list[ ItineraryAttractionRecord ] | None = None,
      visit_date_is_changing: bool = False ) -> list[ AttractionDiff ]:
   diffs: list[ AttractionDiff ] = []

   for attraction_name in attractions:
      carryover = itinerary_attraction_save_carryover(
         saved_attraction_rows,
         attraction_name,
         old_visit_date=old_visit_date )

      new_likelihood = attraction_coordinator.get_attraction_likelihood_for_visit_date(
         visit_date=new_visit_date,
         attraction_name=attraction_name )
      start_time, end_time = (
         ( carryover.start_time, carryover.end_time )
         if visit_date_is_changing
         else cleared_schedule_times_for_visit_window(
            carryover.start_time,
            carryover.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ) )

      diffs.append(
         AttractionDiff(
            name=carryover.name,
            old_likelihood=carryover.old_likelihood,
            new_likelihood=new_likelihood,
            start_time=start_time,
            end_time=end_time,
         )
      )

   return diffs


def _timed_legs_for_transportation_save(
      conn: Connection,
      transportation_name: str,
      visit_date: date,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      carryover_legs: list[ ItineraryTransportationLeg ],
      visit_date_is_changing: bool,
      added_as_attraction: bool,
) -> tuple[ ScheduleTimeKey, list[ ItineraryTransportationLeg ] ]:
   if start_time is None:
      return None, []

   if not visit_date_is_changing:
      return end_time, list( carryover_legs )

   day_loop = fetch_transportation_day_loop(
      conn,
      transportation=transportation_name,
      target_date=visit_date )

   if day_loop is None:
      return end_time, []

   timed_legs, expanded_end_time = expand_timed_transportation_legs(
      transportation=transportation_name,
      start_time=start_time,
      legs=day_loop.legs,
      added_as_attraction=added_as_attraction )

   return expanded_end_time, timed_legs


def validate_itinerary_transportations(
      attraction_coordinator: type[ AttractionCoordinator ],
      conn: Connection,
      transportations: list[ ItineraryTransportationInput ],
      new_visit_date: date,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey,
      old_visit_date: DateKey | None = None,
      saved_transportation_rows: list[ ItineraryTransportationRecord ] | None = None,
      visit_date_is_changing: bool = False ) -> list[ TransportationDiff ]:
   diffs: list[ TransportationDiff ] = []

   for transportation in transportations:
      carryover = itinerary_transportation_save_carryover(
         saved_transportation_rows,
         transportation,
         old_visit_date=old_visit_date )

      new_likelihood = attraction_coordinator.get_attraction_likelihood_for_visit_date(
         visit_date=new_visit_date,
         attraction_name=transportation.name )
      start_time, end_time = (
         ( carryover.start_time, carryover.end_time )
         if visit_date_is_changing
         else cleared_schedule_times_for_visit_window(
            carryover.start_time,
            carryover.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ) )
      end_time, legs = _timed_legs_for_transportation_save(
         conn,
         transportation_name=transportation.name,
         visit_date=new_visit_date,
         start_time=start_time,
         end_time=end_time,
         carryover_legs=carryover.legs,
         visit_date_is_changing=visit_date_is_changing,
         added_as_attraction=transportation.added_as_attraction )

      if not legs:
         diffs.append(
            TransportationDiff(
               name=carryover.name,
               old_likelihood=carryover.old_likelihood,
               new_likelihood=new_likelihood,
               start_time=start_time,
               end_time=end_time,
               legs=legs,
               added_as_attraction=transportation.added_as_attraction,
            )
         )
         continue

      route = resolve_transportation_route_for_date(
         conn,
         transportation=transportation.name,
         target_date=new_visit_date,
      )
      diffs.append(
         TransportationDiff(
            name=carryover.name,
            old_likelihood=carryover.old_likelihood,
            new_likelihood=new_likelihood,
            start_time=start_time,
            end_time=end_time,
            legs=legs,
            route=route,
            route_marker_sequences=build_transportation_route_marker_sequences(
               conn,
               transportation=transportation.name,
               route=route,
               legs=legs,
            ),
            added_as_attraction=transportation.added_as_attraction,
         )
      )

   return diffs


def split_attraction_names_for_itinerary_save(
      conn: Connection,
      attraction_names: list[ str ],
) -> tuple[ list[ str ], list[ str ] ]:
   from ..data_access.attraction_also_transportation import (
      fetch_also_transportation_attraction_names )

   also_transportation_names = fetch_also_transportation_attraction_names( conn )
   plain_attractions: list[ str ] = []
   transportations: list[ str ] = []

   for name in attraction_names:
      if name in also_transportation_names:
         transportations.append( name )
      else:
         plain_attractions.append( name )

   return plain_attractions, transportations



def guardians_talk_diffs_within_visit_window(
      guardians_talks: list[ GuardiansTalkDiff ],
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> list[ GuardiansTalkDiff ]:
   return [
      talk
      for talk in guardians_talks
      if not schedule_time_occurs_outside_visit_window(
            talk.start_time,
            talk.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time )
   ]



def wild_encounter_diffs_within_visit_window(
      wild_encounters: list[ WildEncounterDiff ],
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> list[ WildEncounterDiff ]:
   return [
      encounter
      for encounter in wild_encounters
      if not schedule_time_occurs_outside_visit_window(
            encounter.start_time,
            encounter.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time )
   ]



def itinerary_events_from_saved_rows(
      event_rows: list[ ItineraryEventRecord ],
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> list[ ItineraryEvent ]:
   events: list[ ItineraryEvent ] = []

   for event in event_rows:
      if event.event_type in (
            ItineraryEventType.ARRIVAL,
            ItineraryEventType.DEPARTURE ):
         continue

      if schedule_time_occurs_outside_visit_window(
            event.start_time,
            event.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ):
         continue

      events.append(
         ItineraryEvent(
            event_type=event.event_type,
            start_time=event.start_time,
            end_time=event.end_time,
         )
      )

   return events



def validate_itinerary_for_save(
      conn: Connection,
      save_input: ItinerarySaveInput,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      *,
      new_visit_date_temp: float | None = None,
      old_visit_date: DateKey | None = None ) -> ValidatedItinerary:
   arrival_time = save_input.arrival_time
   saved_itinerary = fetch_saved_itinerary( conn )
   has_saved_itinerary = old_visit_date is not None
   visit_date_is_changing = (
      has_saved_itinerary
      and old_visit_date != save_input.date.isoformat() )
   guardians_talk_diffs = validate_guardians_talks_for_itinerary(
      save_input.guardians_talks,
      guardians_coordinator.get_guardians_talk_schedule(
         month=save_input.month(),
         day=save_input.day(),
         year=save_input.year() ) )
   wild_encounter_diffs = validate_wild_encounters_for_itinerary(
      save_input.wild_encounters,
      wild_encounter_coordinator.get_wild_encounter_schedule(
         month=save_input.month(),
         day=save_input.day(),
         year=save_input.year() ) )
   departure_time = save_input.departure_time
   fixed_time_activity_start_times = [
      *(
         talk.start_time
         for talk in guardians_talk_diffs
         if not talk.is_deleted
      ),
      *(
         encounter.start_time
         for encounter in wild_encounter_diffs
         if not encounter.is_deleted
      ),
   ]
   fixed_time_activity_end_times = [
      *(
         talk.end_time
         for talk in guardians_talk_diffs
         if not talk.is_deleted
      ),
      *(
         encounter.end_time
         for encounter in wild_encounter_diffs
         if not encounter.is_deleted
      ),
   ]

   if not visit_date_is_changing:
      arrival_time = arrival_time_covering_schedule_starts(
         arrival_time,
         fixed_time_activity_start_times )
      departure_time = departure_time_covering_schedule_ends(
         departure_time,
         fixed_time_activity_end_times )

   validated_animals = validate_itinerary_animals(
      animal_coordinator,
      animals=save_input.animals,
      new_visit_date=save_input.date,
      arrival_time=arrival_time,
      departure_time=departure_time,
      new_visit_date_temp=new_visit_date_temp,
      old_visit_date=old_visit_date,
      saved_animal_rows=saved_itinerary.animal_rows,
      visit_date_is_changing=visit_date_is_changing )

   if visit_date_is_changing:
      validated_animals = apply_selected_exhibit_animals_on_date_change(
         animal_coordinator,
         existing_animals=validated_animals,
         selected_exhibits=save_input.selected_exhibits,
         previously_selected_exhibits=saved_itinerary.selected_exhibits,
         saved_animal_rows=saved_itinerary.animal_rows,
         visit_date=save_input.date,
         old_visit_date=old_visit_date,
         visit_date_temp=new_visit_date_temp )

   if validated_animals:
      validated_animals = uncover_animals_for_unavailable_talks(
         conn,
         validated_animals,
         guardians_talk_diffs )
      kept_attraction_names = save_input.attractions or []
      removed_attraction_rows = [
         attraction_row
         for attraction_row in saved_itinerary.attraction_rows
         if attraction_row.attraction not in kept_attraction_names
      ]
      validated_animals = uncover_animals_for_removed_attractions(
         conn,
         validated_animals,
         removed_attraction_rows )

   plain_attraction_names, _diverted_transportation_names = (
      split_attraction_names_for_itinerary_save(
         conn,
         save_input.attractions or [] )
   )
   transportation_inputs = list( save_input.transportations )

   validated_itinerary = ValidatedItinerary(
      arrival_time=arrival_time,
      departure_time=departure_time,
      animals=validated_animals if validated_animals else [],
      attractions=(
         validate_itinerary_attractions(
            attraction_coordinator,
            attractions=plain_attraction_names,
            new_visit_date=save_input.date,
            arrival_time=arrival_time,
            departure_time=departure_time,
            old_visit_date=old_visit_date,
            saved_attraction_rows=saved_itinerary.attraction_rows,
            visit_date_is_changing=visit_date_is_changing )
         if plain_attraction_names
         else [] ),
      transportations=(
         validate_itinerary_transportations(
            attraction_coordinator,
            conn,
            transportations=transportation_inputs,
            new_visit_date=save_input.date,
            arrival_time=arrival_time,
            departure_time=departure_time,
            old_visit_date=old_visit_date,
            saved_transportation_rows=saved_itinerary.transportation_rows,
            visit_date_is_changing=visit_date_is_changing )
         if transportation_inputs
         else [] ),
      guardians_talks=guardians_talk_diffs_within_visit_window(
         guardians_talk_diffs,
         arrival_time=arrival_time,
         departure_time=departure_time ),
      wild_encounters=wild_encounter_diffs_within_visit_window(
         wild_encounter_diffs,
         arrival_time=arrival_time,
         departure_time=departure_time ),
      events=itinerary_events_from_saved_rows(
         saved_itinerary.event_rows,
         arrival_time=arrival_time,
         departure_time=departure_time ),
   )

   return replace(
      validated_itinerary,
      needs_schedule_reschedule=(
         itinerary_needs_schedule_reschedule(
            saved_itinerary,
            validated_itinerary,
            requested_departure_time=save_input.departure_time )
         if has_saved_itinerary
         else False ) )


def itinerary_needs_schedule_reschedule(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary,
      *,
      requested_departure_time: ScheduleTimeKey ) -> bool:
   # Match schedule-item: rebuild when a new talk/encounter overlaps guest
   # schedules. Removals alone do not. Visit-window edits only rebuild when
   # they cut off already-scheduled guest items (e.g. date-change arrival).
   if new_guardians_talks_overlapping_saved_schedule(
         saved_itinerary,
         validated_itinerary ):
      return True

   if new_wild_encounters_overlapping_saved_schedule(
         saved_itinerary,
         validated_itinerary ):
      return True

   if not _visit_window_changed(
         saved_itinerary,
         arrival_time=validated_itinerary.arrival_time,
         departure_time=requested_departure_time ):
      return False

   return _visit_window_cuts_off_saved_schedules(
      saved_itinerary,
      arrival_time=validated_itinerary.arrival_time,
      departure_time=requested_departure_time )


def _visit_window_changed(
      saved_itinerary: SavedItinerary,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> bool:
   return (
      saved_itinerary.arrival_time != arrival_time
      or saved_itinerary.departure_time != departure_time
   )


def _visit_window_cuts_off_saved_schedules(
      saved_itinerary: SavedItinerary,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> bool:
   # Talks and encounters are omitted: if still offered on the new day they keep
   # the same zoo-hours slot (so they stay inside the visit window), and if not
   # offered they are dropped during validation rather than left cut off.
   for animal in saved_itinerary.animal_rows:
      if schedule_time_occurs_outside_visit_window(
            animal.start_time,
            animal.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ):
         return True

   for attraction in saved_itinerary.attraction_rows:
      if schedule_time_occurs_outside_visit_window(
            attraction.start_time,
            attraction.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ):
         return True

   for transportation in saved_itinerary.transportation_rows:
      if schedule_time_occurs_outside_visit_window(
            transportation.start_time,
            transportation.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ):
         return True

   for event in saved_itinerary.event_rows:
      if event.event_type in (
            ItineraryEventType.ARRIVAL,
            ItineraryEventType.DEPARTURE ):
         continue

      if schedule_time_occurs_outside_visit_window(
            event.start_time,
            event.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ):
         return True

   return False

