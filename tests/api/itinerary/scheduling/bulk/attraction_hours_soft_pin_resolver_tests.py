from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.scheduling.bulk.attraction_hours_soft_pin_resolver import AttractionHoursSoftPinResolver
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.shared.operating_hours import OperatingHours


def _loop_unit(
      loop_id: str | None,
      stops: list,
   ) -> LoopScheduleUnit:
   return LoopScheduleUnit(
      loop_id=loop_id,
      stops=stops,
      entry_walk_node_id=None,
      exit_walk_node_id=None,
      side_cluster_id=None,
      loop_index_in_side_cluster=None,
      traversal=None )


def Test_Resolve_TestInvalidVisitDate_ExpectEmpty() -> None:
   assert AttractionHoursSoftPinResolver.resolve(
      object(),
      attractions=[],
      loop_units=[],
      visit_date=None,
      zoo_operating_hours=OperatingHours(
         open_seconds=9 * 3600,
         close_seconds=19 * 3600 ) ) == []


def Test_AttachToWindows_TestNoPins_ExpectSameWindows() -> None:
   windows = [
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=12 * 3600 ),
   ]

   assert AttractionHoursSoftPinResolver.attach_to_windows(
      windows,
      [] ) is windows


def Test_AttachToWindows_TestOverlappingPins_ExpectFilteredByWindow() -> None:
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   morning = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=10 * 3600 )
   afternoon = ItineraryScheduleWindow(
      start_seconds=11 * 3600,
      end_seconds=15 * 3600 )

   attached = AttractionHoursSoftPinResolver.attach_to_windows(
      [ morning, afternoon ],
      [ soft_pin ] )

   assert attached[ 0 ].attraction_hours_soft_pins == []
   assert attached[ 1 ].attraction_hours_soft_pins == [ soft_pin ]


def Test_LoopIdByAttractionName_TestMixedStops_ExpectMappedAttractionLoop() -> None:
   animal = ItineraryAnimalRecord(
      species='Capybara',
      exhibit='Americas Outdoor Mayan Temple Ruins' )
   attraction = ItineraryAttractionRecord(
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )

   loop_ids = AttractionHoursSoftPinResolver._loop_id_by_attraction_name(
      [
         _loop_unit( None, [ attraction ] ),
         _loop_unit( 'zoomobile', [ animal, attraction ] ),
      ] )

   assert loop_ids == { 'Zoomobile': 'zoomobile' }


def Test_StopsBefore_TestUnknownLoop_ExpectEmpty() -> None:
   soft_pin = AttractionHoursSoftPin(
      loop_id='unknown-loop',
      viewing_spot_index=2,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   attraction = ItineraryAttractionRecord(
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )

   assert AttractionHoursSoftPinResolver.stops_before(
      [ attraction ],
      loop_id='unknown-loop',
      soft_pin=soft_pin ) == []


def Test_Resolve_TestAttractionNotOnLoop_ExpectEmpty() -> None:
   soft_pins = AttractionHoursSoftPinResolver.resolve(
      object(),
      attractions=[
         ItineraryAttractionRecord(
            attraction='Zoomobile',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      loop_units=[],
      visit_date='2026-06-20',
      zoo_operating_hours=OperatingHours(
         open_seconds=9 * 3600,
         close_seconds=19 * 3600 ) )

   assert soft_pins == []


def Test_Resolve_TestSplashOnLoopWithHours_ExpectSoftPin(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash = ItineraryAttractionRecord(
      attraction='Splash Island',
      old_likelihood=None,
      new_likelihood=100 )
   hours = OperatingHours(
      open_seconds=12 * 3600,
      close_seconds=17 * 3600 )
   loop_units = [
      _loop_unit(
         'splash',
         [ splash ] ),
   ]

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_hours_soft_pin_resolver.AttractionOperatingHoursResolver.fetch_configured_operating_hours_seconds',
      lambda conn, attraction, *, visit_date, zoo_operating_hours: hours )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_hours_soft_pin_resolver.LoopPinSegmentSplitter.viewing_spot_index_for_stop',
      lambda loop_id, stop: 0 )

   soft_pins = AttractionHoursSoftPinResolver.resolve(
      object(),
      attractions=[ splash ],
      loop_units=loop_units,
      visit_date='2026-06-20',
      zoo_operating_hours=OperatingHours(
         open_seconds=9 * 3600,
         close_seconds=19 * 3600 ) )

   assert soft_pins == [
      AttractionHoursSoftPin(
         loop_id='splash',
         viewing_spot_index=0,
         attraction_name='Splash Island',
         open_seconds=12 * 3600,
         close_seconds=17 * 3600 ),
   ]


def Test_Resolve_TestHoursClosedOrInvalid_ExpectEmpty(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash = ItineraryAttractionRecord(
      attraction='Splash Island',
      old_likelihood=None,
      new_likelihood=100 )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_hours_soft_pin_resolver.AttractionOperatingHoursResolver.fetch_configured_operating_hours_seconds',
      lambda conn, attraction, *, visit_date, zoo_operating_hours: OperatingHours(
         open_seconds=12 * 3600,
         close_seconds=12 * 3600 ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_hours_soft_pin_resolver.LoopPinSegmentSplitter.viewing_spot_index_for_stop',
      lambda loop_id, stop: 0 )

   assert AttractionHoursSoftPinResolver.resolve(
      object(),
      attractions=[ splash ],
      loop_units=[ _loop_unit( 'splash', [ splash ] ) ],
      visit_date='2026-06-20',
      zoo_operating_hours=OperatingHours(
         open_seconds=9 * 3600,
         close_seconds=19 * 3600 ) ) == []

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_hours_soft_pin_resolver.AttractionOperatingHoursResolver.fetch_configured_operating_hours_seconds',
      lambda conn, attraction, *, visit_date, zoo_operating_hours: None )

   assert AttractionHoursSoftPinResolver.resolve(
      object(),
      attractions=[ splash ],
      loop_units=[ _loop_unit( 'splash', [ splash ] ) ],
      visit_date='2026-06-20',
      zoo_operating_hours=OperatingHours(
         open_seconds=9 * 3600,
         close_seconds=19 * 3600 ) ) == []


def Test_Resolve_TestAttractionWithoutViewingSpotIndex_ExpectEmpty(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash = ItineraryAttractionRecord(
      attraction='Splash Island',
      old_likelihood=None,
      new_likelihood=100 )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_hours_soft_pin_resolver.AttractionOperatingHoursResolver.fetch_configured_operating_hours_seconds',
      lambda conn, attraction, *, visit_date, zoo_operating_hours: OperatingHours(
         open_seconds=12 * 3600,
         close_seconds=17 * 3600 ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_hours_soft_pin_resolver.LoopPinSegmentSplitter.viewing_spot_index_for_stop',
      lambda loop_id, stop: None )

   assert AttractionHoursSoftPinResolver.resolve(
      object(),
      attractions=[ splash ],
      loop_units=[ _loop_unit( 'splash', [ splash ] ) ],
      visit_date='2026-06-20',
      zoo_operating_hours=OperatingHours(
         open_seconds=9 * 3600,
         close_seconds=19 * 3600 ) ) == []
