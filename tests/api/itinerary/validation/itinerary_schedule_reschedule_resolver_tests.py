from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.validation.itinerary_schedule_reschedule_resolver import ItineraryScheduleRescheduleResolver
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryEventType
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


AFRICAN_LION = 'African Lion'
AFRICA_SAVANNA = 'Africa Savanna'
GREVYS_ZEBRA = "Grevy's Zebra"
CONSERVATION_CAROUSEL = 'Conservation Carousel'
GRIZZLY_BEAR = 'Grizzly Bear'
VISIT_DATE = '2026-06-15'
DEFAULT_ARRIVAL_TIME = '9:30 AM'
DEFAULT_DEPARTURE_TIME = '5:00 PM'
ANIMAL_DURATION_MINUTES = 8
TALK_DURATION_MINUTES = 30
ENCOUNTER_DURATION_MINUTES = 45
LUNCH_DURATION_MINUTES = 30
TRANSPORTATION_DURATION_MINUTES = 15
ANIMAL_LIKELIHOOD = 100


def _saved(
      *,
      arrival_time: str = DEFAULT_ARRIVAL_TIME,
      departure_time: str = DEFAULT_DEPARTURE_TIME,
      animal_start: str | None = '11:00 AM',
      animal_end: str | None = None ) -> SavedItinerary:
   if animal_end is None and animal_start is not None:
      animal_end = DateValues.add_minutes_to_time(
         animal_start,
         ANIMAL_DURATION_MINUTES )

   return SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=arrival_time,
      departure_time=departure_time,
      animal_rows=[
         ItineraryAnimalRecord(
            species=AFRICAN_LION,
            exhibit=AFRICA_SAVANNA,
            old_likelihood=None,
            new_likelihood=ANIMAL_LIKELIHOOD,
            start_time=animal_start,
            end_time=animal_end ),
      ],
   )


def _validated(
      *,
      arrival_time: str = DEFAULT_ARRIVAL_TIME,
      talk: GuardiansTalkDiff | None = None ) -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time=arrival_time,
      departure_time=DEFAULT_DEPARTURE_TIME,
      animals=[],
      attractions=[],
      guardians_talks=[ talk ] if talk is not None else [],
      wild_encounters=[],
      events=[],
   )


def Test_NeedsReschedule_TestNewTalkOverlapsSaved_ExpectTrue() -> None:
   saved = _saved()
   animal = saved.animal_rows[ Position.FIRST ]
   talk = GuardiansTalkDiff(
      name=GREVYS_ZEBRA,
      is_deleted=False,
      start_time=animal.start_time,
      end_time=DateValues.add_minutes_to_time(
         animal.start_time,
         TALK_DURATION_MINUTES ) )
   validated = _validated( talk=talk )
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestVisitWindowCutsOffAnimal_ExpectTrue() -> None:
   saved = _saved()
   later_arrival = '12:00 PM'
   validated = _validated( arrival_time=later_arrival )
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestUnchangedWindow_ExpectFalse() -> None:
   saved = _saved()
   validated = _validated()
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is False


def Test_NeedsReschedule_TestChangedWindowWithoutCutoff_ExpectFalse() -> None:
   saved = _saved( animal_start='12:00 PM' )
   earlier_arrival = '11:00 AM'
   validated = _validated( arrival_time=earlier_arrival )
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is False


def Test_NeedsReschedule_TestDepartureCutsOffAnimal_ExpectTrue() -> None:
   saved = _saved( animal_start='4:30 PM' )
   validated = _validated()
   requested_departure_time = '4:15 PM'

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestDepartureCutsOffEvent_ExpectTrue() -> None:
   lunch_start = '4:30 PM'
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=DEFAULT_ARRIVAL_TIME,
      departure_time=DEFAULT_DEPARTURE_TIME,
      event_rows=[
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time=lunch_start,
            end_time=DateValues.add_minutes_to_time(
               lunch_start,
               LUNCH_DURATION_MINUTES ) ),
      ],
   )
   validated = _validated()
   requested_departure_time = '4:15 PM'

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestDepartureCutsOffAttraction_ExpectTrue() -> None:
   attraction_start = '4:30 PM'
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=DEFAULT_ARRIVAL_TIME,
      departure_time=DEFAULT_DEPARTURE_TIME,
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction=CONSERVATION_CAROUSEL,
            old_likelihood=None,
            new_likelihood=None,
            start_time=attraction_start,
            end_time=DateValues.add_minutes_to_time(
               attraction_start,
               ANIMAL_DURATION_MINUTES ) ),
      ],
   )
   validated = _validated()
   requested_departure_time = '4:15 PM'

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestRemovedWildEncounter_ExpectFalse() -> None:
   animal_start = '10:00 AM'
   encounter_start = '3:30 PM'
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=DEFAULT_ARRIVAL_TIME,
      departure_time=DEFAULT_DEPARTURE_TIME,
      animal_rows=[
         ItineraryAnimalRecord(
            species=AFRICAN_LION,
            exhibit=AFRICA_SAVANNA,
            old_likelihood=None,
            new_likelihood=ANIMAL_LIKELIHOOD,
            start_time=animal_start,
            end_time=DateValues.add_minutes_to_time(
               animal_start,
               ANIMAL_DURATION_MINUTES ) ),
      ],
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter=GRIZZLY_BEAR,
            start_time=encounter_start,
            end_time=DateValues.add_minutes_to_time(
               encounter_start,
               ENCOUNTER_DURATION_MINUTES ),
            is_deleted=False ),
      ],
   )
   validated = _validated()
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is False


def Test_NeedsReschedule_TestRemovedGuardiansTalk_ExpectFalse() -> None:
   animal_start = '10:00 AM'
   talk_start = '11:00 AM'
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=DEFAULT_ARRIVAL_TIME,
      departure_time=DEFAULT_DEPARTURE_TIME,
      animal_rows=[
         ItineraryAnimalRecord(
            species=AFRICAN_LION,
            exhibit=AFRICA_SAVANNA,
            old_likelihood=None,
            new_likelihood=ANIMAL_LIKELIHOOD,
            start_time=animal_start,
            end_time=DateValues.add_minutes_to_time(
               animal_start,
               ANIMAL_DURATION_MINUTES ) ),
      ],
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name=GREVYS_ZEBRA,
            start_time=talk_start,
            end_time=DateValues.add_minutes_to_time(
               talk_start,
               TALK_DURATION_MINUTES ),
            is_deleted=False ),
      ],
   )
   validated = _validated()
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is False


def Test_NeedsReschedule_TestLaterArrivalWithoutCutoff_ExpectFalse() -> None:
   saved = _saved( animal_start='11:00 AM' )
   later_arrival = '10:00 AM'
   validated = _validated( arrival_time=later_arrival )
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is False


def Test_NeedsReschedule_TestLaterArrivalCutsOffAnimal_ExpectTrue() -> None:
   saved = _saved( animal_start='10:00 AM' )
   later_arrival = '10:30 AM'
   validated = _validated( arrival_time=later_arrival )
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestDateChangeEarlyAdmissionToStandardOpen_ExpectTrue() -> None:
   early_arrival = '9:00 AM'
   animal_start = DateValues.add_minutes_to_time(
      early_arrival,
      ANIMAL_DURATION_MINUTES )
   saved = _saved(
      arrival_time=early_arrival,
      animal_start=animal_start )
   standard_open = '9:30 AM'
   validated = _validated( arrival_time=standard_open )
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestDateChangeShorterCloseCutsOffEveningAnimal_ExpectTrue() -> None:
   saved = _saved(
      departure_time='8:00 PM',
      animal_start='6:30 PM' )
   validated = _validated()
   requested_departure_time = '18:00'

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestNewWildEncounterOverlapsSaved_ExpectTrue() -> None:
   animal_start = '10:00 AM'
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=DEFAULT_ARRIVAL_TIME,
      departure_time=DEFAULT_DEPARTURE_TIME,
      animal_rows=[
         ItineraryAnimalRecord(
            species=AFRICAN_LION,
            exhibit=AFRICA_SAVANNA,
            old_likelihood=None,
            new_likelihood=ANIMAL_LIKELIHOOD,
            start_time=animal_start,
            end_time=DateValues.add_minutes_to_time(
               animal_start,
               ANIMAL_DURATION_MINUTES ) ),
      ],
   )
   encounter = WildEncounterDiff(
      name=GRIZZLY_BEAR,
      is_deleted=False,
      start_time=animal_start,
      end_time=DateValues.add_minutes_to_time(
         animal_start,
         ENCOUNTER_DURATION_MINUTES ),
      meeting_spot='Spot',
      link='' )
   validated = ValidatedItinerary(
      arrival_time=saved.arrival_time,
      departure_time=saved.departure_time,
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ encounter ],
      events=[],
   )
   requested_departure_time = saved.departure_time

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestDepartureCutsOffTransportation_ExpectTrue() -> None:
   ride_start = '4:30 PM'
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=DEFAULT_ARRIVAL_TIME,
      departure_time=DEFAULT_DEPARTURE_TIME,
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation=TransportationName.ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=None,
            added_as_attraction=False,
            start_time=ride_start,
            end_time=DateValues.add_minutes_to_time(
               ride_start,
               TRANSPORTATION_DURATION_MINUTES ) ),
      ],
   )
   validated = _validated()
   requested_departure_time = '4:15 PM'

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is True


def Test_NeedsReschedule_TestDepartureCutsOffArrivalEvent_ExpectFalse() -> None:
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=DEFAULT_ARRIVAL_TIME,
      departure_time=DEFAULT_DEPARTURE_TIME,
      event_rows=[
         ItineraryEventRecord(
            event_type=ItineraryEventType.ARRIVAL,
            start_time=DEFAULT_ARRIVAL_TIME,
            end_time=DEFAULT_ARRIVAL_TIME ),
      ],
   )
   later_arrival = '10:00 AM'
   validated = _validated( arrival_time=later_arrival )
   requested_departure_time = '4:15 PM'

   needs_reschedule = ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time=requested_departure_time )

   assert needs_reschedule is False
