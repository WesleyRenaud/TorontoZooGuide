from __future__ import annotations

from dataclasses import replace

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.validated_itinerary import ValidatedItinerary
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...guardians.itinerary.guardians_talk_itinerary_validator import GuardiansTalkItineraryValidator
from .itinerary_animal_validator import ItineraryAnimalValidator
from .itinerary_attraction_validator import ItineraryAttractionValidator
from .itinerary_save_attraction_split_builder import ItinerarySaveAttractionSplitBuilder
from .itinerary_schedule_reschedule_resolver import ItineraryScheduleRescheduleResolver
from .itinerary_transportation_validator import ItineraryTransportationValidator
from .itinerary_visit_window_content_builder import ItineraryVisitWindowContentBuilder
from ..scheduling.bulk.attraction_animal_coverer import AttractionAnimalCoverer
from ..scheduling.bulk.guardians_talk_animal_coverer import GuardiansTalkAnimalCoverer
from ..scheduling.extend_departure_for_activity import arrival_time_covering_schedule_starts
from ..scheduling.extend_departure_for_activity import departure_time_covering_schedule_ends
from .selected_exhibit_date_change_animals_builder import SelectedExhibitDateChangeAnimalsBuilder
from ...types import Connection, DateKey
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ...wild_encounters.itinerary.wild_encounter_itinerary_validator import WildEncounterItineraryValidator


class ItinerarySaveValidator():
   @classmethod
   def validate_for_save(
         cls,
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
      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
      has_saved_itinerary = old_visit_date is not None
      visit_date_is_changing = (
         has_saved_itinerary
         and old_visit_date != save_input.date.isoformat() )
      guardians_talk_diffs = GuardiansTalkItineraryValidator.validate_for_itinerary(
         save_input.guardians_talks,
         guardians_coordinator.get_guardians_talk_schedule(
            month=save_input.month(),
            day=save_input.day(),
            year=save_input.year() ) )
      wild_encounter_diffs = WildEncounterItineraryValidator.validate_for_itinerary(
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

      validated_animals = ItineraryAnimalValidator.validate(
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
         validated_animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
            animal_coordinator,
            existing_animals=validated_animals,
            selected_exhibits=save_input.selected_exhibits,
            previously_selected_exhibits=saved_itinerary.selected_exhibits,
            saved_animal_rows=saved_itinerary.animal_rows,
            visit_date=save_input.date,
            old_visit_date=old_visit_date,
            visit_date_temp=new_visit_date_temp )

      if validated_animals:
         validated_animals = GuardiansTalkAnimalCoverer.uncover_for_unavailable_talks(
            conn,
            validated_animals,
            guardians_talk_diffs )
         kept_attraction_names = save_input.attractions or []
         removed_attraction_rows = [
            attraction_row
            for attraction_row in saved_itinerary.attraction_rows
            if attraction_row.attraction not in kept_attraction_names
         ]
         validated_animals = AttractionAnimalCoverer.uncover_for_removed(
            conn,
            validated_animals,
            removed_attraction_rows )

      plain_attraction_names, _diverted_transportation_names = (
         ItinerarySaveAttractionSplitBuilder.split_names(
            conn,
            save_input.attractions or [] )
      )
      transportation_inputs = list( save_input.transportations )

      validated_itinerary = ValidatedItinerary(
         arrival_time=arrival_time,
         departure_time=departure_time,
         animals=validated_animals if validated_animals else [],
         attractions=(
            ItineraryAttractionValidator.validate(
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
            ItineraryTransportationValidator.validate(
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
         guardians_talks=ItineraryVisitWindowContentBuilder.filter_guardians_talks(
            guardians_talk_diffs,
            arrival_time=arrival_time,
            departure_time=departure_time ),
         wild_encounters=ItineraryVisitWindowContentBuilder.filter_wild_encounters(
            wild_encounter_diffs,
            arrival_time=arrival_time,
            departure_time=departure_time ),
         events=ItineraryVisitWindowContentBuilder.events_from_saved_rows(
            saved_itinerary.event_rows,
            arrival_time=arrival_time,
            departure_time=departure_time ),
      )

      return replace(
         validated_itinerary,
         needs_schedule_reschedule=(
            ItineraryScheduleRescheduleResolver.needs_reschedule(
               saved_itinerary,
               validated_itinerary,
               requested_departure_time=save_input.departure_time )
            if has_saved_itinerary
            else False ) )
