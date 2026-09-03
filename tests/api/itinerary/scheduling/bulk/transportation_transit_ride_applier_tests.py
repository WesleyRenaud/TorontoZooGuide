from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.data_access.itinerary_transportation_provider import ItineraryTransportationProvider
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.bulk.planned_transit_ride import PlannedTransitRide
from api.itinerary.scheduling.bulk.scheduled_animal_anchor import ScheduledAnimalAnchor
from api.itinerary.scheduling.bulk.transportation_transit_ride_applier import TransportationTransitRideApplier
from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_day_loop_fetcher import TransportationDayLoopFetcher
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.operating_hours import OperatingHours
from api.transportation.data_access.transportation_station_record import TransportationStationRecord
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.shortest_path import WalkGraphAdjacency
from api.walk_graph.walk_graph_adjacency_builder import WalkGraphAdjacencyBuilder


ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'

VISIT_DATE = date( 2026, 7, 11 )

SUMMER_DAY_LOOP = TransportationDayLoop(
   transportation=ZOOMOBILE,
   route='summer',
   main_station=MAIN,
   legs=[
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      TransportationRouteLegSegment( AFRICA, TUNDRA, 15 ),
      TransportationRouteLegSegment( TUNDRA, EURASIA, 15 ),
      TransportationRouteLegSegment( EURASIA, MAIN, 15 ),
   ],
)

TRANSIT_APPLIER_SCHEMA = """
CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT        NOT NULL,
   OLD_LIKELIHOOD           INTEGER,
   NEW_LIKELIHOOD           INTEGER,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   START_TIME               TEXT,
   END_TIME                 TEXT,
   ROUTE                    TEXT,
   BULK_TRANSIT_EVALUATED   INTEGER     NOT NULL DEFAULT 0
);
"""


def _px( minutes: float ) -> float:
   return minutes * WalkTravelTimeCalculator.WALK_PX_PER_MINUTE


def _node( node_id: str, x_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': 0.0,
      'x_px': x_px,
      'y_px': 0.0,
   }


def _bidirectional_edges(
      edges: list[ dict[ str, object ] ],
   ) -> list[ dict[ str, object ] ]:
   paired: list[ dict[ str, object ] ] = []

   for edge in edges:
      paired.append( edge )
      paired.append(
         {
            'from': edge[ 'to' ],
            'to': edge[ 'from' ],
            'length_px': edge[ 'length_px' ],
         } )

   return paired


def _domain_walk_graph() -> WalkGraph:
   return {
      'map_width_px': 10000,
      'map_height_px': 100,
      'entrance_node_id': 'n-entrance',
      'nodes': [
         _node( 'n-entrance', 0.0 ),
         _node( 'n-main', _px( 1 ) ),
         _node( 'n-canada', _px( 16 ) ),
         _node( 'n-africa', _px( 21 ) ),
         _node( 'n-tundra', _px( 26 ) ),
         _node( 'n-eurasia', _px( 31 ) ),
         _node( 'n-domain', _px( 36 ) ),
      ],
      'edges': _bidirectional_edges( [
         { 'from': 'n-entrance', 'to': 'n-main', 'length_px': _px( 1 ) },
         { 'from': 'n-main', 'to': 'n-canada', 'length_px': _px( 15 ) },
         { 'from': 'n-canada', 'to': 'n-africa', 'length_px': _px( 5 ) },
         { 'from': 'n-africa', 'to': 'n-tundra', 'length_px': _px( 5 ) },
         { 'from': 'n-tundra', 'to': 'n-eurasia', 'length_px': _px( 5 ) },
         { 'from': 'n-eurasia', 'to': 'n-main', 'length_px': _px( 30 ) },
         { 'from': 'n-africa', 'to': 'n-domain', 'length_px': _px( 15 ) },
         { 'from': 'n-entrance', 'to': 'n-domain', 'length_px': _px( 36 ) },
      ] ),
   }


def _north_cluster_walk_graph() -> WalkGraph:
   return {
      'map_width_px': 10000,
      'map_height_px': 100,
      'entrance_node_id': 'n-entrance',
      'nodes': [
         _node( 'n-entrance', 0.0 ),
         _node( 'n-main', _px( 2 ) ),
         _node( 'n-canada', _px( 12 ) ),
         _node( 'n-africa', _px( 22 ) ),
         _node( 'n-tundra', _px( 32 ) ),
         _node( 'n-australasia', _px( 37 ) ),
         _node( 'n-eurasia', _px( 42 ) ),
         _node( 'n-tundra-animal', _px( 33 ) ),
         _node( 'n-australasia-animal', _px( 38 ) ),
         _node( 'n-eurasia-animal', _px( 43 ) ),
      ],
      'edges': _bidirectional_edges( [
         { 'from': 'n-entrance', 'to': 'n-main', 'length_px': _px( 2 ) },
         { 'from': 'n-main', 'to': 'n-canada', 'length_px': _px( 10 ) },
         { 'from': 'n-canada', 'to': 'n-africa', 'length_px': _px( 10 ) },
         { 'from': 'n-africa', 'to': 'n-tundra', 'length_px': _px( 10 ) },
         { 'from': 'n-tundra', 'to': 'n-australasia', 'length_px': _px( 5 ) },
         { 'from': 'n-australasia', 'to': 'n-eurasia', 'length_px': _px( 5 ) },
         { 'from': 'n-eurasia', 'to': 'n-main', 'length_px': _px( 40 ) },
         { 'from': 'n-tundra', 'to': 'n-tundra-animal', 'length_px': _px( 1 ) },
         { 'from': 'n-australasia', 'to': 'n-australasia-animal', 'length_px': _px( 1 ) },
         { 'from': 'n-eurasia', 'to': 'n-eurasia-animal', 'length_px': _px( 1 ) },
      ] ),
   }


def _station_walk_nodes( graph: WalkGraph ) -> dict[ str, str ]:
   return {
      MAIN: 'n-main',
      CANADA: 'n-canada',
      AFRICA: 'n-africa',
      TUNDRA: 'n-tundra',
      EURASIA: 'n-eurasia',
   }


def _insert_zoomobile_transit( conn: sqlite3.Connection ) -> None:
   cur = conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=False )
   conn.commit()
   cur.close()


@pytest.fixture
def applier_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSIT_APPLIER_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


def Test_TransitTimelineStart_TestScheduleAnchorOnly_ExpectEntranceNode() -> None:
   timeline_start, start_node_id = TransportationTransitRideApplier._transit_timeline_start(
      None,
      schedule_anchor_seconds=9 * 3600 + 30 * 60,
      station_walk_nodes={ MAIN: 'n-main' },
      entrance_node_id='n-entrance' )

   assert timeline_start == 9 * 3600 + 30 * 60
   assert start_node_id == 'n-entrance'


def Test_TransitTimelineStart_TestAfterAttractionTrip_ExpectAlightNodeAndAnchorSeconds() -> None:
   companion = ItineraryTransportationRecord(
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True,
      start_time='10:00 AM',
      end_time='11:15 AM',
      legs=[
         ItineraryTransportationLeg(
            MAIN,
            CANADA,
            '10:00 AM',
            '10:20 AM',
            ZOOMOBILE,
            True ),
      ],
   )

   timeline_start, start_node_id = TransportationTransitRideApplier._transit_timeline_start(
      companion,
      schedule_anchor_seconds=9 * 3600,
      station_walk_nodes={ MAIN: 'n-main', CANADA: 'n-canada' },
      entrance_node_id='n-entrance' )

   assert timeline_start == 11 * 3600 + 15 * 60
   assert start_node_id == 'n-canada'


def Test_TransitTimelineStart_TestCompanionEndsBeforeAnchor_ExpectAnchorSeconds() -> None:
   companion = ItineraryTransportationRecord(
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True,
      start_time='9:00 AM',
      end_time='9:15 AM',
      legs=[],
   )

   timeline_start, start_node_id = TransportationTransitRideApplier._transit_timeline_start(
      companion,
      schedule_anchor_seconds=9 * 3600 + 30 * 60,
      station_walk_nodes={ MAIN: 'n-main' },
      entrance_node_id='n-entrance' )

   assert timeline_start == 9 * 3600 + 30 * 60
   assert start_node_id == 'n-entrance'


def Test_RideWindowWithinOperatingHours_TestBeforeOpen_ExpectShiftedToOpen() -> None:
   operating_hours = OperatingHours(
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )

   window = TransportationTransitRideApplier._ride_window_within_operating_hours(
      9 * 3600 + 45 * 60,
      20 * 60,
      operating_hours )

   assert window == ( 10 * 3600, 10 * 3600 + 20 * 60 )


def Test_RideWindowWithinOperatingHours_TestEndsAfterClose_ExpectNone() -> None:
   operating_hours = OperatingHours(
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )

   assert TransportationTransitRideApplier._ride_window_within_operating_hours(
      17 * 3600 + 45 * 60,
      20 * 60,
      operating_hours ) is None


def Test_BestSavingRide_TestLongWalkToDomain_ExpectMainBoardingRide() -> None:
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )

   ride = TransportationTransitRideApplier._best_saving_ride(
      day_loop=SUMMER_DAY_LOOP,
      station_walk_nodes={
         MAIN: 'n-main',
         CANADA: 'n-canada',
         AFRICA: 'n-africa',
         TUNDRA: 'n-tundra',
         EURASIA: 'n-eurasia',
      },
      from_node_id='n-entrance',
      to_node_id='n-domain',
      walk_graph=walk_graph,
      adjacency=adjacency )

   assert ride is not None
   assert ride.from_station == MAIN
   assert ride.to_station in { CANADA, AFRICA }


def Test_PlanRidesForAnchors_TestDomainVisit_ExpectOutboundAndReturnToMain() -> None:
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )
   anchors = [
      ScheduledAnimalAnchor(
         animal=ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100 ),
         walk_node_id='n-domain',
         duration_seconds=8 * 60 ),
   ]

   rides_before, return_ride = TransportationTransitRideApplier._plan_rides_for_anchors(
      day_loop=SUMMER_DAY_LOOP,
      station_walk_nodes={
         MAIN: 'n-main',
         CANADA: 'n-canada',
         AFRICA: 'n-africa',
         TUNDRA: 'n-tundra',
         EURASIA: 'n-eurasia',
      },
      start_node_id='n-entrance',
      entrance_node_id='n-entrance',
      animal_anchors=anchors,
      walk_graph=walk_graph,
      adjacency=adjacency )

   assert rides_before[ 0 ] is not None
   assert rides_before[ 0 ].from_station == MAIN
   assert return_ride is not None
   assert return_ride.to_station == MAIN


def Test_PlanRidesForAnchors_TestNorthClusterAnchors_ExpectNoEurasiaToTundraRide() -> None:
   walk_graph = _north_cluster_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )
   anchors = [
      ScheduledAnimalAnchor(
         animal=ItineraryAnimalRecord(
            species='Polar Bear',
            exhibit='Tundra Trek',
            old_likelihood=None,
            new_likelihood=100 ),
         walk_node_id='n-tundra-animal',
         duration_seconds=8 * 60 ),
      ScheduledAnimalAnchor(
         animal=ItineraryAnimalRecord(
            species='Western Grey Kangaroo',
            exhibit='Australasia Outdoor',
            old_likelihood=None,
            new_likelihood=100 ),
         walk_node_id='n-australasia-animal',
         duration_seconds=8 * 60 ),
      ScheduledAnimalAnchor(
         animal=ItineraryAnimalRecord(
            species='Amur Tiger',
            exhibit='Eurasia Wilds',
            old_likelihood=None,
            new_likelihood=100 ),
         walk_node_id='n-eurasia-animal',
         duration_seconds=8 * 60 ),
   ]

   rides_before, return_ride = TransportationTransitRideApplier._plan_rides_for_anchors(
      day_loop=SUMMER_DAY_LOOP,
      station_walk_nodes=_station_walk_nodes( walk_graph ),
      start_node_id='n-entrance',
      entrance_node_id='n-entrance',
      animal_anchors=anchors,
      walk_graph=walk_graph,
      adjacency=adjacency )

   planned_rides = [ ride for ride in [ *rides_before, return_ride ] if ride is not None ]

   assert planned_rides
   assert not any(
      ride.from_station == EURASIA and ride.to_station == TUNDRA
      for ride in planned_rides )


def Test_Apply_TestEmptyInputs_ExpectEarlyReturn(
      applier_conn: sqlite3.Connection ) -> None:
   TransportationTransitRideApplier.apply(
      applier_conn,
      transit_rows=[],
      scheduled_animals=[
         ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
      visit_date='2026-07-11',
      schedule_anchor_seconds=9 * 3600 )

   TransportationTransitRideApplier.apply(
      applier_conn,
      transit_rows=[
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False ),
      ],
      scheduled_animals=[],
      visit_date='2026-07-11',
      schedule_anchor_seconds=9 * 3600 )

   TransportationTransitRideApplier.apply(
      applier_conn,
      transit_rows=[
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False ),
      ],
      scheduled_animals=[
         ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
      visit_date=None,
      schedule_anchor_seconds=9 * 3600 )


def Test_AnimalAnchors_TestTimedAnimalsSorted_ExpectAnchorsWithDurations(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walk_graph = _domain_walk_graph()
   early = ItineraryAnimalRecord(
      species='Wood Bison',
      exhibit='Canadian Domain',
      old_likelihood=None,
      new_likelihood=100,
      start_time='11:00 AM',
      end_time='11:08 AM' )
   late = ItineraryAnimalRecord(
      species='Polar Bear',
      exhibit='Tundra Trek',
      old_likelihood=None,
      new_likelihood=100,
      start_time='1:00 PM',
      end_time='1:20 PM' )
   untimed = ItineraryAnimalRecord(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=None,
      new_likelihood=100 )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.BulkScheduleWalkOrderBuilder.representative_walk_node_id',
      lambda walk_graph, entrance_node_id, species, exhibit, enclosure_name: {
         'Wood Bison': 'n-domain',
         'Polar Bear': 'n-tundra',
      }.get( species ) )

   anchors = TransportationTransitRideApplier._animal_anchors(
      walk_graph,
      'n-entrance',
      [ late, untimed, early ] )

   assert [ anchor.animal.species for anchor in anchors ] == [ 'Wood Bison', 'Polar Bear' ]
   assert anchors[ 0 ].walk_node_id == 'n-domain'
   assert anchors[ 0 ].duration_seconds == 8 * 60
   assert anchors[ 1 ].duration_seconds == 20 * 60


def Test_AnimalAnchors_TestMissingWalkNode_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animal = ItineraryAnimalRecord(
      species='Wood Bison',
      exhibit='Canadian Domain',
      old_likelihood=None,
      new_likelihood=100,
      start_time='11:00 AM',
      end_time='11:08 AM' )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.BulkScheduleWalkOrderBuilder.representative_walk_node_id',
      lambda *_args, **_kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ViewingSpotWalkNodeIdResolver.resolve',
      lambda *_args, **_kwargs: None )

   assert TransportationTransitRideApplier._animal_anchors(
      _domain_walk_graph(),
      'n-entrance',
      [ animal ] ) == []


def Test_StationWalkNodeIds_TestRouteStationsSnapped_ExpectStationMap(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.TransportationStationProvider.fetch_transportation_station_records',
      lambda conn, transportation: [
         TransportationStationRecord(
            name=MAIN,
            description='',
            x_coord=0.0,
            y_coord=0.0 ),
         TransportationStationRecord(
            name=CANADA,
            description='',
            x_coord=1.0,
            y_coord=0.0 ),
         TransportationStationRecord(
            name='Closed Station',
            description='',
            x_coord=2.0,
            y_coord=0.0 ),
      ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.WalkNodeSnapper.snap',
      lambda x_coord, y_coord, walk_graph: (
         { 0.0: 'n-main', 1.0: 'n-canada' }[ x_coord ],
         0.0,
      ) )

   station_nodes = TransportationTransitRideApplier._station_walk_node_ids(
      applier_conn,
      transportation=ZOOMOBILE,
      day_loop=SUMMER_DAY_LOOP,
      walk_graph=_domain_walk_graph() )

   assert station_nodes == {
      MAIN: 'n-main',
      CANADA: 'n-canada',
   }


def Test_WalkSecondsToStation_TestMissingStation_ExpectZero() -> None:
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )

   assert TransportationTransitRideApplier._walk_seconds_to_station(
      walk_graph=walk_graph,
      adjacency=adjacency,
      station_walk_nodes={ MAIN: 'n-main' },
      from_node_id='n-entrance',
      station_name=CANADA ) == 0


def Test_ApplyTimeline_TestRidePastAnimalStart_ExpectShiftBumpAndPersisted(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animal = ItineraryAnimalRecord(
      species='Wood Bison',
      exhibit='Canadian Domain',
      old_likelihood=None,
      new_likelihood=100,
      start_time='11:00 AM',
      end_time='11:08 AM' )
   transit_row = ItineraryTransportationRecord(
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=False )
   ride = PlannedTransitRide(
      from_station=MAIN,
      to_station=AFRICA,
      legs=[
         TransportationRouteLegSegment( MAIN, CANADA, 20 ),
         TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      ],
      remaining_walk_px=1.0 )
   animal_updates: list[ tuple[ str, str, str ] ] = []
   ride_segments: list[ object ] = []
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )

   monkeypatch.setattr(
      TransportationTransitRideApplier,
      '_walk_seconds_to_station',
      lambda **_kwargs: 0 )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ScheduleItineraryItemProvider.update_itinerary_animal_schedule',
      lambda cur, *, species, exhibit, enclosure_name, start_time, end_time: (
         animal_updates.append( ( species, start_time, end_time ) ) or True ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ScheduleItineraryTransportationProvider.apply_itinerary_transportation_ride_segments',
      lambda cur, *, name, added_as_attraction, route, segments: (
         ride_segments.extend( segments ) or True ) )

   # Timeline starts at 10:40 AM; 30-minute ride ends at 11:10 AM, past 11:00 AM animal start.
   TransportationTransitRideApplier._apply_timeline(
      applier_conn,
      transit_row=transit_row,
      day_loop=SUMMER_DAY_LOOP,
      animal_anchors=[
         ScheduledAnimalAnchor(
            animal=animal,
            walk_node_id='n-domain',
            duration_seconds=8 * 60 ),
      ],
      rides_before_animals=[ ride ],
      return_ride=None,
      timeline_start_seconds=10 * 3600 + 40 * 60,
      start_node_id='n-entrance',
      walk_graph=walk_graph,
      adjacency=adjacency,
      station_walk_nodes=_station_walk_nodes( walk_graph ),
      operating_hours=None )

   assert animal_updates == [ ( 'Wood Bison', '11:10 AM', '11:18 AM' ) ]
   assert len( ride_segments ) == 1
   assert ride_segments[ 0 ][ 0 ] == '10:40 AM'
   assert ride_segments[ 0 ][ 1 ] == list( ride.legs )


def Test_ApplyTimeline_TestNoSegments_ExpectNoPersist(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animal = ItineraryAnimalRecord(
      species='Wood Bison',
      exhibit='Canadian Domain',
      old_likelihood=None,
      new_likelihood=100,
      start_time='11:00 AM',
      end_time='11:08 AM' )
   persist_calls: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ScheduleItineraryItemProvider.update_itinerary_animal_schedule',
      lambda *_args, **_kwargs: persist_calls.append( 'animal' ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ScheduleItineraryTransportationProvider.apply_itinerary_transportation_ride_segments',
      lambda *_args, **_kwargs: persist_calls.append( 'ride' ) )

   TransportationTransitRideApplier._apply_timeline(
      applier_conn,
      transit_row=ItineraryTransportationRecord(
         transportation=ZOOMOBILE,
         old_likelihood=None,
         new_likelihood=100,
         added_as_attraction=False ),
      day_loop=SUMMER_DAY_LOOP,
      animal_anchors=[
         ScheduledAnimalAnchor(
            animal=animal,
            walk_node_id='n-domain',
            duration_seconds=8 * 60 ),
      ],
      rides_before_animals=[ None ],
      return_ride=None,
      timeline_start_seconds=9 * 3600,
      start_node_id='n-entrance',
      walk_graph=_domain_walk_graph(),
      adjacency=WalkGraphAdjacencyBuilder.build( _domain_walk_graph() ),
      station_walk_nodes={},
      operating_hours=None )

   assert persist_calls == []


def Test_Apply_TestNoRideSegments_ExpectBulkTransitEvaluatedFlag(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   WalkGraphProvider.fetch.cache_clear()
   cur = applier_conn.cursor()
   ItineraryTransportationProvider.insert_itinerary_transportation(
      cur,
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=False )
   applier_conn.commit()
   cur.close()

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: _domain_walk_graph() )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: SUMMER_DAY_LOOP )
   monkeypatch.setattr(
      TransportationTransitRideApplier,
      '_station_walk_node_ids',
      lambda conn, *, transportation, day_loop, walk_graph: {
         MAIN: 'n-main',
         CANADA: 'n-canada',
         AFRICA: 'n-africa',
         TUNDRA: 'n-tundra',
         EURASIA: 'n-eurasia',
      } )
   monkeypatch.setattr(
      TransportationTransitRideApplier,
      '_animal_anchors',
      lambda walk_graph, entrance_node_id, scheduled_animals: [
         ScheduledAnimalAnchor(
            animal=scheduled_animals[ 0 ],
            walk_node_id='n-domain',
            duration_seconds=8 * 60 ),
      ] )
   monkeypatch.setattr(
      TransportationTransitRideApplier,
      '_plan_rides_for_anchors',
      lambda **_kwargs: ( [], None ) )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-07-11',
         arrival_time='9:00 AM',
         departure_time='6:00 PM',
      ) )

   TransportationTransitRideApplier.apply(
      applier_conn,
      transit_rows=[
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False ),
      ],
      scheduled_animals=[
         ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
      visit_date='2026-07-11',
      schedule_anchor_seconds=9 * 3600 )

   row = applier_conn.execute(
      """   SELECT BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 0;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert row is not None
   assert row[ 'BULK_TRANSIT_EVALUATED' ] == 1


def Test_Apply_TestInvalidVisitDate_ExpectSkipped(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   WalkGraphProvider.fetch.cache_clear()
   _insert_zoomobile_transit( applier_conn )
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: _domain_walk_graph() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.DateValues.parse_date_value',
      lambda visit_date: None )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-07-11',
         arrival_time='9:00 AM',
         departure_time='6:00 PM',
      ) )

   TransportationTransitRideApplier.apply(
      applier_conn,
      transit_rows=[
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False ),
      ],
      scheduled_animals=[
         ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
      visit_date='not-a-date',
      schedule_anchor_seconds=9 * 3600 )

   row = applier_conn.execute(
      """   SELECT BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert row is not None
   assert row[ 'BULK_TRANSIT_EVALUATED' ] == 0


def Test_Apply_TestDayLoopMissing_ExpectSkipped(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   WalkGraphProvider.fetch.cache_clear()
   _insert_zoomobile_transit( applier_conn )
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: _domain_walk_graph() )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: None )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-07-11',
         arrival_time='9:00 AM',
         departure_time='6:00 PM',
      ) )

   TransportationTransitRideApplier.apply(
      applier_conn,
      transit_rows=[
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False ),
      ],
      scheduled_animals=[
         ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
      visit_date='2026-07-11',
      schedule_anchor_seconds=9 * 3600 )

   row = applier_conn.execute(
      """   SELECT BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert row is not None
   assert row[ 'BULK_TRANSIT_EVALUATED' ] == 0


def Test_Apply_TestNoStationNodes_ExpectSkipped(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   WalkGraphProvider.fetch.cache_clear()
   _insert_zoomobile_transit( applier_conn )
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: _domain_walk_graph() )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: SUMMER_DAY_LOOP )
   monkeypatch.setattr(
      TransportationTransitRideApplier,
      '_station_walk_node_ids',
      lambda conn, *, transportation, day_loop, walk_graph: {} )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-07-11',
         arrival_time='9:00 AM',
         departure_time='6:00 PM',
      ) )

   TransportationTransitRideApplier.apply(
      applier_conn,
      transit_rows=[
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False ),
      ],
      scheduled_animals=[
         ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
      visit_date='2026-07-11',
      schedule_anchor_seconds=9 * 3600 )

   row = applier_conn.execute(
      """   SELECT BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert row is not None
   assert row[ 'BULK_TRANSIT_EVALUATED' ] == 0


def Test_Apply_TestNoAnimalAnchors_ExpectSkipped(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   WalkGraphProvider.fetch.cache_clear()
   _insert_zoomobile_transit( applier_conn )
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: _domain_walk_graph() )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: SUMMER_DAY_LOOP )
   monkeypatch.setattr(
      TransportationTransitRideApplier,
      '_station_walk_node_ids',
      lambda conn, *, transportation, day_loop, walk_graph: {
         MAIN: 'n-main',
         AFRICA: 'n-africa',
      } )
   monkeypatch.setattr(
      TransportationTransitRideApplier,
      '_animal_anchors',
      lambda walk_graph, entrance_node_id, scheduled_animals: [] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-07-11',
         arrival_time='9:00 AM',
         departure_time='6:00 PM',
      ) )

   TransportationTransitRideApplier.apply(
      applier_conn,
      transit_rows=[
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False ),
      ],
      scheduled_animals=[
         ItineraryAnimalRecord(
            species='Wood Bison',
            exhibit='Canadian Domain',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM',
         ),
      ],
      visit_date='2026-07-11',
      schedule_anchor_seconds=9 * 3600 )

   row = applier_conn.execute(
      """   SELECT BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert row is not None
   assert row[ 'BULK_TRANSIT_EVALUATED' ] == 0


def Test_BestSavingRide_TestSameNode_ExpectNone() -> None:
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )

   assert TransportationTransitRideApplier._best_saving_ride(
      day_loop=SUMMER_DAY_LOOP,
      station_walk_nodes=_station_walk_nodes( walk_graph ),
      from_node_id='n-main',
      to_node_id='n-main',
      walk_graph=walk_graph,
      adjacency=adjacency ) is None


def Test_BestSavingRide_TestUnreachableBoardNode_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )

   def distance(
         graph: WalkGraph,
         from_node_id: str,
         to_node_id: str,
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> float | None:
      if to_node_id == 'n-canada':
         return None
      return 100.0

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ShortestPathCalculator.distance',
      distance )

   assert TransportationTransitRideApplier._best_saving_ride(
      day_loop=SUMMER_DAY_LOOP,
      station_walk_nodes=_station_walk_nodes( walk_graph ),
      from_node_id='n-entrance',
      to_node_id='n-domain',
      walk_graph=walk_graph,
      adjacency=adjacency ) is None


def Test_BestSavingRide_TestNoRouteLegs_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.TransportationDayLoopLegSelector.select',
      lambda day_loop, board_station, alight_station: [] )

   assert TransportationTransitRideApplier._best_saving_ride(
      day_loop=SUMMER_DAY_LOOP,
      station_walk_nodes=_station_walk_nodes( walk_graph ),
      from_node_id='n-entrance',
      to_node_id='n-domain',
      walk_graph=walk_graph,
      adjacency=adjacency ) is None


def Test_BestSavingRide_TestRemainingWalkTooLong_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ShortestPathCalculator.distance',
      lambda graph, from_node_id, to_node_id, *, adjacency=None: (
         100.0 if from_node_id == to_node_id else 1000.0 ) )

   assert TransportationTransitRideApplier._best_saving_ride(
      day_loop=SUMMER_DAY_LOOP,
      station_walk_nodes=_station_walk_nodes( walk_graph ),
      from_node_id='n-entrance',
      to_node_id='n-domain',
      walk_graph=walk_graph,
      adjacency=adjacency ) is None


def Test_BestSavingRide_TestUnreachableDestinationFromAlight_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )
   short_day_loop = TransportationDayLoop(
      transportation=ZOOMOBILE,
      route='summer',
      main_station=MAIN,
      legs=[
         TransportationRouteLegSegment( MAIN, CANADA, 2 ),
         TransportationRouteLegSegment( CANADA, AFRICA, 2 ),
      ],
   )

   def distance(
         graph: WalkGraph,
         from_node_id: str,
         to_node_id: str,
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> float | None:
      if from_node_id == 'n-entrance' and to_node_id == 'n-domain':
         return 300.0
      if to_node_id == 'n-domain' and from_node_id != 'n-domain':
         return None
      if from_node_id == to_node_id:
         return 0.0
      return 20.0

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ShortestPathCalculator.distance',
      distance )

   assert TransportationTransitRideApplier._best_saving_ride(
      day_loop=short_day_loop,
      station_walk_nodes=_station_walk_nodes( walk_graph ),
      from_node_id='n-entrance',
      to_node_id='n-domain',
      walk_graph=walk_graph,
      adjacency=adjacency ) is None


def Test_WalkSecondsToStation_TestKnownStation_ExpectWalkSeconds() -> None:
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )

   assert TransportationTransitRideApplier._walk_seconds_to_station(
      walk_graph=walk_graph,
      adjacency=adjacency,
      station_walk_nodes={ MAIN: 'n-main' },
      from_node_id='n-entrance',
      station_name=MAIN ) > 0


def Test_ApplyTimeline_TestUntimedAnimal_ExpectSkipped(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animal = ItineraryAnimalRecord(
      species='Wood Bison',
      exhibit='Canadian Domain',
      old_likelihood=None,
      new_likelihood=100 )
   persist_calls: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ScheduleItineraryItemProvider.update_itinerary_animal_schedule',
      lambda *_args, **_kwargs: persist_calls.append( 'animal' ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ScheduleItineraryTransportationProvider.apply_itinerary_transportation_ride_segments',
      lambda *_args, **_kwargs: persist_calls.append( 'ride' ) )

   TransportationTransitRideApplier._apply_timeline(
      applier_conn,
      transit_row=ItineraryTransportationRecord(
         transportation=ZOOMOBILE,
         old_likelihood=None,
         new_likelihood=100,
         added_as_attraction=False ),
      day_loop=SUMMER_DAY_LOOP,
      animal_anchors=[
         ScheduledAnimalAnchor(
            animal=animal,
            walk_node_id='n-domain',
            duration_seconds=8 * 60 ),
      ],
      rides_before_animals=[ None ],
      return_ride=None,
      timeline_start_seconds=9 * 3600,
      start_node_id='n-entrance',
      walk_graph=_domain_walk_graph(),
      adjacency=WalkGraphAdjacencyBuilder.build( _domain_walk_graph() ),
      station_walk_nodes={},
      operating_hours=None )

   assert persist_calls == []


def Test_ApplyTimeline_TestReturnRide_ExpectReturnSegmentPersisted(
      applier_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animal = ItineraryAnimalRecord(
      species='Wood Bison',
      exhibit='Canadian Domain',
      old_likelihood=None,
      new_likelihood=100,
      start_time='11:00 AM',
      end_time='11:08 AM' )
   transit_row = ItineraryTransportationRecord(
      transportation=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=False )
   outbound = PlannedTransitRide(
      from_station=MAIN,
      to_station=AFRICA,
      legs=[
         TransportationRouteLegSegment( MAIN, CANADA, 20 ),
         TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      ],
      remaining_walk_px=1.0 )
   return_ride = PlannedTransitRide(
      from_station=AFRICA,
      to_station=MAIN,
      legs=[
         TransportationRouteLegSegment( AFRICA, TUNDRA, 15 ),
         TransportationRouteLegSegment( TUNDRA, EURASIA, 15 ),
         TransportationRouteLegSegment( EURASIA, MAIN, 15 ),
      ],
      remaining_walk_px=0.0 )
   ride_segments: list[ object ] = []
   walk_graph = _domain_walk_graph()
   adjacency = WalkGraphAdjacencyBuilder.build( walk_graph )

   monkeypatch.setattr(
      TransportationTransitRideApplier,
      '_walk_seconds_to_station',
      lambda **_kwargs: 0 )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ScheduleItineraryItemProvider.update_itinerary_animal_schedule',
      lambda cur, *, species, exhibit, enclosure_name, start_time, end_time: True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_ride_applier.ScheduleItineraryTransportationProvider.apply_itinerary_transportation_ride_segments',
      lambda cur, *, name, added_as_attraction, route, segments: (
         ride_segments.extend( segments ) or True ) )

   TransportationTransitRideApplier._apply_timeline(
      applier_conn,
      transit_row=transit_row,
      day_loop=SUMMER_DAY_LOOP,
      animal_anchors=[
         ScheduledAnimalAnchor(
            animal=animal,
            walk_node_id='n-domain',
            duration_seconds=8 * 60 ),
      ],
      rides_before_animals=[ outbound ],
      return_ride=return_ride,
      timeline_start_seconds=10 * 3600 + 40 * 60,
      start_node_id='n-entrance',
      walk_graph=walk_graph,
      adjacency=adjacency,
      station_walk_nodes=_station_walk_nodes( walk_graph ),
      operating_hours=None )

   assert len( ride_segments ) == 2
   assert ride_segments[ 1 ][ 1 ] == list( return_ride.legs )
