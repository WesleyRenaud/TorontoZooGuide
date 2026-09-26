from __future__ import annotations

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.core.itinerary_activity_scheduler import ItineraryActivityScheduler
from api.models import Animal
from api.models import Attraction
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import WildEncounter
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItemType, ItineraryEventType, Position


def Test_ScheduleActivities_TestAllItemKinds_ExpectTimesAndLunchEvent() -> None:
   animal = Animal( species='Lion', exhibit='Savanna' )
   attraction = Attraction( name='Carousel', free_with_admission=True )
   talk = GuardiansTalk(
      name='Rhino Talk',
      location='Rhino House',
      x_coord=1.0,
      y_coord=2.0 )
   encounter = WildEncounter(
      name='Capybara',
      meeting_spot='Mayan Temple Meeting Spot',
      link='capybara' )
   animal_start = '10:00'
   animal_end = '10:20'
   attraction_start = '11:00'
   attraction_end = '11:30'
   talk_start = '12:00'
   talk_end = '12:30'
   encounter_start = '13:00'
   encounter_end = '13:45'
   lunch_start = '14:00'
   lunch_end = '14:30'
   itinerary = Itinerary(
      date='2026-06-15',
      animals=[ animal ],
      attractions=[ attraction ],
      guardians_talks=[ talk ],
      wild_encounters=[ encounter ] )
   scheduler = ItineraryActivityScheduler( itinerary )

   animal_scheduled = scheduler.schedule_animal(
      animal.species,
      animal.exhibit,
      animal_start,
      animal_end )
   attraction_scheduled = scheduler.schedule_attraction(
      attraction.name,
      attraction_start,
      attraction_end )
   talk_scheduled = scheduler.schedule_guardians_talk(
      talk.name,
      talk_start,
      talk_end )
   encounter_scheduled = scheduler.schedule_wild_encounter(
      encounter.name,
      encounter_start,
      encounter_end )
   scheduler.schedule_event( ItineraryEventType.LUNCH, lunch_start, lunch_end )
   lunch = itinerary.events[ Position.FIRST ]

   assert animal_scheduled
   assert attraction_scheduled
   assert talk_scheduled
   assert encounter_scheduled
   assert itinerary.animals[ Position.FIRST ].start_time == DateValues.normalize_schedule_time(
      animal_start )
   assert itinerary.attractions[ Position.FIRST ].end_time == DateValues.normalize_schedule_time(
      attraction_end )
   assert itinerary.guardians_talks[ Position.FIRST ].start_time == DateValues.normalize_schedule_time(
      talk_start )
   assert itinerary.wild_encounters[ Position.FIRST ].end_time == DateValues.normalize_schedule_time(
      encounter_end )
   assert lunch.to_dict() == {
      'event_type': ItineraryEventType.LUNCH.value,
      'start_time': DateValues.normalize_schedule_time( lunch_start ),
      'end_time': DateValues.normalize_schedule_time( lunch_end ),
      'type': ItemType.ITINERARY_EVENT.value,
   }


def Test_ScheduleAnimal_TestUnknownAnimal_ExpectFalse() -> None:
   itinerary = ItineraryBuilder.empty()
   scheduler = ItineraryActivityScheduler( itinerary )

   scheduled = scheduler.schedule_animal( 'Lion', 'Savanna', '10:00', '10:20' )

   assert not scheduled


def Test_ScheduleAttraction_TestUnknownAttraction_ExpectFalse() -> None:
   itinerary = ItineraryBuilder.empty()
   scheduler = ItineraryActivityScheduler( itinerary )

   scheduled = scheduler.schedule_attraction( 'Carousel', '11:00', '11:30' )

   assert not scheduled


def Test_ScheduleGuardiansTalk_TestUnknownTalk_ExpectFalse() -> None:
   itinerary = ItineraryBuilder.empty()
   scheduler = ItineraryActivityScheduler( itinerary )

   scheduled = scheduler.schedule_guardians_talk( 'Rhino Talk', '12:00', '12:30' )

   assert not scheduled


def Test_ScheduleWildEncounter_TestUnknownEncounter_ExpectFalse() -> None:
   itinerary = ItineraryBuilder.empty()
   scheduler = ItineraryActivityScheduler( itinerary )

   scheduled = scheduler.schedule_wild_encounter( 'Capybara', '13:00', '13:45' )

   assert not scheduled
