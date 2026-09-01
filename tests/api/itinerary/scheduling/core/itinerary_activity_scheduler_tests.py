from __future__ import annotations

from api.itinerary.scheduling.core.itinerary_activity_scheduler import ItineraryActivityScheduler
from api.models import Animal
from api.models import Attraction
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import WildEncounter
from api.shared.enums import ItineraryEventType


def Test_ScheduleActivities_TestAllItemKinds_ExpectTimesAndLunchEvent() -> None:
   itinerary = Itinerary(
      date='2026-06-15',
      animals=[ Animal( species='Lion', exhibit='Savanna' ) ],
      attractions=[ Attraction( name='Carousel', free_with_admission=True ) ],
      guardians_talks=[
         GuardiansTalk(
            name='Rhino Talk',
            location='Rhino House',
            x_coord=1.0,
            y_coord=2.0 )
      ],
      wild_encounters=[
         WildEncounter(
            name='Capybara',
            meeting_spot='Mayan Temple Meeting Spot',
            link='capybara' )
      ] )
   scheduler = ItineraryActivityScheduler( itinerary )

   assert scheduler.schedule_animal( 'Lion', 'Savanna', '10:00', '10:20' )
   assert scheduler.schedule_attraction( 'Carousel', '11:00', '11:30' )
   assert scheduler.schedule_guardians_talk( 'Rhino Talk', '12:00', '12:30' )
   assert scheduler.schedule_wild_encounter( 'Capybara', '13:00', '13:45' )

   scheduler.schedule_event( ItineraryEventType.LUNCH, '14:00', '14:30' )

   assert itinerary.animals[ 0 ].start_time == '10:00 AM'
   assert itinerary.attractions[ 0 ].end_time == '11:30 AM'
   assert itinerary.guardians_talks[ 0 ].start_time == '12:00 PM'
   assert itinerary.wild_encounters[ 0 ].end_time == '1:45 PM'
   assert itinerary.events[ 0 ].to_dict() == {
      'event_type': 'lunch',
      'start_time': '2:00 PM',
      'end_time': '2:30 PM',
      'type': 'itineraryEvent',
   }
