from __future__ import annotations

from typing import Any

from api_test_support.coordinator_call import CoordinatorCall

from api.itinerary.operations.suppress_itinerary_warning_result import SuppressItineraryWarningResult
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.results.itinerary_time_set_result import ItineraryTimeSetResult
from api.models import Itinerary


class StubItineraryCoordinator:
   instances: list[ StubItineraryCoordinator ] = []
   default_success: bool = True
   calls: list[ CoordinatorCall ]
   closed: bool


   def __init__( self ) -> None:
      self.calls = []
      self.closed = False
      StubItineraryCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def set_itinerary( self, **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( CoordinatorCall( 'set_itinerary', kwargs ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def schedule_itinerary_item(
         self,
         schedule_item_key: Any = None,
         **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( CoordinatorCall(
         'schedule_itinerary_item',
         {
            'schedule_item_key': schedule_item_key,
            **kwargs,
         },
      ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def bulk_schedule_itinerary( self, **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( CoordinatorCall( 'bulk_schedule_itinerary', kwargs ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def unschedule_all_itinerary_items( self, **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( CoordinatorCall( 'unschedule_all_itinerary_items', kwargs ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def get_itinerary_date( self ) -> str:
      self.calls.append( CoordinatorCall( 'get_itinerary_date', {} ) )
      return '2026-06-15'


   def get_itinerary( self, **kwargs: Any ) -> Itinerary:
      self.calls.append( CoordinatorCall( 'get_itinerary', kwargs ) )
      return Itinerary( date='2026-06-15' )


   def set_arrival_time( self, **kwargs: Any ) -> ItineraryTimeSetResult:
      self.calls.append( CoordinatorCall( 'set_arrival_time', kwargs ) )
      return ItineraryTimeSetResult(
         itinerary=Itinerary(
            date='2026-06-15',
            arrival_time=kwargs.get( 'arrival_time' ),
         ) )


   def set_departure_time( self, **kwargs: Any ) -> ItineraryTimeSetResult:
      self.calls.append( CoordinatorCall( 'set_departure_time', kwargs ) )
      return ItineraryTimeSetResult(
         itinerary=Itinerary(
            date='2026-06-15',
            departure_time=kwargs.get( 'departure_time' ),
         ) )


   def unschedule_itinerary_item(
         self,
         schedule_item_key: Any = None,
         **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( CoordinatorCall(
         'unschedule_itinerary_item',
         {
            'schedule_item_key': schedule_item_key,
            **kwargs,
         },
      ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def remove_itinerary_item(
         self,
         schedule_item_key: Any = None,
         **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( CoordinatorCall(
         'remove_itinerary_item',
         {
            'schedule_item_key': schedule_item_key,
            **kwargs,
         },
      ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def suppress_itinerary_warning(
         self,
         **kwargs: Any ) -> SuppressItineraryWarningResult:
      self.calls.append( CoordinatorCall( 'suppress_itinerary_warning', kwargs ) )
      return SuppressItineraryWarningResult()


   def unsuppress_itinerary_warning(
         self,
         **kwargs: Any ) -> SuppressItineraryWarningResult:
      self.calls.append( CoordinatorCall( 'unsuppress_itinerary_warning', kwargs ) )
      return SuppressItineraryWarningResult()


   def accept_itinerary( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'AcceptItineraryProvider.accept_itinerary', kwargs ) )
      return type( self ).default_success


   def clear_itinerary( self ) -> bool:
      self.calls.append( CoordinatorCall( 'ClearItineraryProvider.clear_itinerary', {} ) )
      return type( self ).default_success
