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
from api.shared.enums import ItineraryEventType


def _saved(
      *,
      arrival_time: str = '9:30 AM',
      departure_time: str = '5:00 PM',
      animal_start: str | None = '11:00 AM',
      animal_end: str | None = '11:08 AM' ) -> SavedItinerary:
   return SavedItinerary(
      date_value='2026-06-15',
      arrival_time=arrival_time,
      departure_time=departure_time,
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time=animal_start,
            end_time=animal_end ),
      ],
   )


def _validated(
      *,
      arrival_time: str = '9:30 AM',
      talk: GuardiansTalkDiff | None = None ) -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time=arrival_time,
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[ talk ] if talk is not None else [],
      wild_encounters=[],
      events=[],
   )


def Test_NeedsReschedule_TestNewTalkOverlapsSaved_ExpectTrue() -> None:
   talk = GuardiansTalkDiff(
      name="Grevy's Zebra",
      is_deleted=False,
      start_time='11:00 AM',
      end_time='11:30 AM' )

   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      _saved(),
      _validated( talk=talk ),
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestVisitWindowCutsOffAnimal_ExpectTrue() -> None:
   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      _saved(),
      _validated( arrival_time='12:00 PM' ),
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestUnchangedWindow_ExpectFalse() -> None:
   assert not ItineraryScheduleRescheduleResolver.needs_reschedule(
      _saved(),
      _validated(),
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestChangedWindowWithoutCutoff_ExpectFalse() -> None:
   assert not ItineraryScheduleRescheduleResolver.needs_reschedule(
      _saved( animal_start='12:00 PM', animal_end='12:08 PM' ),
      _validated( arrival_time='11:00 AM' ),
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestDepartureCutsOffAnimal_ExpectTrue() -> None:
   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      _saved( animal_start='4:30 PM', animal_end='4:38 PM' ),
      _validated(),
      requested_departure_time='4:15 PM' )


def Test_NeedsReschedule_TestDepartureCutsOffEvent_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      event_rows=[
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='4:30 PM',
            end_time='5:00 PM',
         ),
      ],
   )

   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      _validated(),
      requested_departure_time='4:15 PM' )


def Test_NeedsReschedule_TestDepartureCutsOffAttraction_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=None,
            start_time='4:30 PM',
            end_time='4:38 PM',
         ),
      ],
   )

   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      _validated(),
      requested_departure_time='4:15 PM' )


def Test_NeedsReschedule_TestRemovedWildEncounter_ExpectFalse() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM',
         ),
      ],
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter='Grizzly Bear',
            start_time='3:30 PM',
            end_time='4:15 PM',
            is_deleted=False,
         ),
      ],
   )

   assert not ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      _validated(),
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestRemovedGuardiansTalk_ExpectFalse() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM',
         ),
      ],
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name="Grevy's Zebra",
            start_time='11:00 AM',
            end_time='11:30 AM',
            is_deleted=False,
         ),
      ],
   )

   assert not ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      _validated(),
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestLaterArrivalWithoutCutoff_ExpectFalse() -> None:
   assert not ItineraryScheduleRescheduleResolver.needs_reschedule(
      _saved( animal_start='11:00 AM', animal_end='11:08 AM' ),
      _validated( arrival_time='10:00 AM' ),
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestLaterArrivalCutsOffAnimal_ExpectTrue() -> None:
   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      _saved( animal_start='10:00 AM', animal_end='10:08 AM' ),
      _validated( arrival_time='10:30 AM' ),
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestDateChangeEarlyAdmissionToStandardOpen_ExpectTrue() -> None:
   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      _saved(
         arrival_time='9:00 AM',
         animal_start='9:08 AM',
         animal_end='9:16 AM',
      ),
      _validated( arrival_time='9:30 AM' ),
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestDateChangeShorterCloseCutsOffEveningAnimal_ExpectTrue() -> None:
   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      _saved(
         departure_time='8:00 PM',
         animal_start='6:30 PM',
         animal_end='6:38 PM',
      ),
      _validated(),
      requested_departure_time='18:00' )


def Test_NeedsReschedule_TestNewWildEncounterOverlapsSaved_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM',
         ),
      ],
   )
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         WildEncounterDiff(
            name='Grizzly Bear',
            is_deleted=False,
            start_time='10:00 AM',
            end_time='10:45 AM',
            meeting_spot='Spot',
            link='' ),
      ],
      events=[],
   )

   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      validated,
      requested_departure_time='5:00 PM' )


def Test_NeedsReschedule_TestDepartureCutsOffTransportation_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=None,
            added_as_attraction=False,
            start_time='4:30 PM',
            end_time='4:45 PM',
         ),
      ],
   )

   assert ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      _validated(),
      requested_departure_time='4:15 PM' )


def Test_NeedsReschedule_TestDepartureCutsOffArrivalEvent_ExpectFalse() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      event_rows=[
         ItineraryEventRecord(
            event_type=ItineraryEventType.ARRIVAL,
            start_time='9:30 AM',
            end_time='9:30 AM',
         ),
      ],
   )

   assert not ItineraryScheduleRescheduleResolver.needs_reschedule(
      saved,
      _validated( arrival_time='10:00 AM' ),
      requested_departure_time='4:15 PM' )
