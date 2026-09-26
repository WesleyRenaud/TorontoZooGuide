from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator import BulkRescheduleLongWaitSimulator
from api.itinerary.warnings.guardians_talk_long_wait_warning_builder import GuardiansTalkLongWaitWarningBuilder
from api.models import Animal
from api.models import GuardiansTalk
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType


ZEBRA_TALK = "Grevy's Zebra"
MEERKAT_TALK = 'Slender-Tailed Meerkat'


def Test_IsolatedFromItinerary_TestTalkFarFromItems_ExpectIsolatedTalk() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   nearby_start = '10:15 AM'
   nearby_duration_minutes = 30
   far_start = '1:00 PM'
   far_duration_minutes = 30
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   nearby = GuardiansTalk(
      name=ZEBRA_TALK,
      location='Africa Savanna',
      x_coord=0.0,
      y_coord=0.0,
      start_time=nearby_start,
      end_time=DateValues.add_minutes_to_time( nearby_start, nearby_duration_minutes ) )
   far = GuardiansTalk(
      name=MEERKAT_TALK,
      location='African Rainforest Pavilion',
      x_coord=0.0,
      y_coord=0.0,
      start_time=far_start,
      end_time=DateValues.add_minutes_to_time( far_start, far_duration_minutes ) )
   itinerary.guardians_talks = [ nearby, far ]

   isolated = GuardiansTalkLongWaitWarningBuilder.isolated_from_itinerary( itinerary )

   assert [ talk.name for talk in isolated ] == [ far.name ]


def Test_IsolatedFromItinerary_TestTalkNearItems_ExpectEmpty() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   talk_start = '10:15 AM'
   talk_duration_minutes = 30
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time=talk_start,
         end_time=DateValues.add_minutes_to_time( talk_start, talk_duration_minutes ) ),
   ]

   isolated = GuardiansTalkLongWaitWarningBuilder.isolated_from_itinerary( itinerary )

   assert isolated == []


def Test_ReasonAfterAddingWithSimulatedBulk_TestNotIsolated_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      'is_isolated_after_adding',
      lambda *args, **kwargs: False )
   talk = GuardiansTalkDiff( name=ZEBRA_TALK, is_deleted=False )
   itinerary_context: dict = {}

   issue = GuardiansTalkLongWaitWarningBuilder.reason_after_adding_with_simulated_bulk(
      None,
      talk,
      itinerary_context=itinerary_context )

   assert issue is None


def Test_ReasonAfterAddingWithSimulatedBulk_TestIsolated_ExpectIssue(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      'is_isolated_after_adding',
      lambda *args, **kwargs: True )
   start_time = '1:00 PM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   itinerary_context: dict = {}

   issue = GuardiansTalkLongWaitWarningBuilder.reason_after_adding_with_simulated_bulk(
      None,
      talk,
      itinerary_context=itinerary_context )

   assert issue is not None
   assert issue.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
