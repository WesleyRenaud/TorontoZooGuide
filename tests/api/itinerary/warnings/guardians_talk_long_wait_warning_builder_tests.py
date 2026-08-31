from __future__ import annotations

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.warnings.guardians_talk_long_wait_warning_builder import GuardiansTalkLongWaitWarningBuilder
from api.models import Animal
from api.models import GuardiansTalk
from api.shared.constants import Constants


ZEBRA_TALK = "Grevy's Zebra"
MEERKAT_TALK = 'Slender-Tailed Meerkat'


def Test_IsolatedFromItinerary_TestTalkFarFromItems_ExpectIsolatedTalk() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='10:15 AM',
         end_time='10:45 AM' ),
      GuardiansTalk(
         name=MEERKAT_TALK,
         location='African Rainforest Pavilion',
         x_coord=0.0,
         y_coord=0.0,
         start_time='1:00 PM',
         end_time='1:30 PM' ),
   ]

   isolated = GuardiansTalkLongWaitWarningBuilder.isolated_from_itinerary( itinerary )

   assert [ talk.name for talk in isolated ] == [ MEERKAT_TALK ]
   assert Constants.MAX_FIXED_TIME_ITEM_WAIT_MINUTES == 30


def Test_IsolatedFromItinerary_TestTalkNearItems_ExpectEmpty() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='10:15 AM',
         end_time='10:45 AM' ),
   ]

   assert GuardiansTalkLongWaitWarningBuilder.isolated_from_itinerary( itinerary ) == []
