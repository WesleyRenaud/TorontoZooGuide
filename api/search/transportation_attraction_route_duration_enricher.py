from __future__ import annotations

from datetime import date

from ..itinerary.transportation.transportation_route_duration_resolver import TransportationRouteDurationResolver
from ..models import Attraction
from ..request_connection_provider import RequestConnectionProvider
from ..shared.calendar_dates import CalendarDates
from ..types import Types


class TransportationAttractionRouteDurationEnricher():
   @classmethod
   def enrich(
         cls,
         attractions: list[ Attraction ],
         *,
         target_date: date,
   ) -> None:
      conn = RequestConnectionProvider.get()

      for attraction in attractions:
         if not attraction.is_also_transportation:
            continue

         attraction.route_duration_minutes = TransportationRouteDurationResolver.minutes(
            conn,
            transportation=attraction.name,
            target_date=target_date,
         )


   @classmethod
   def enrich_for_visit(
         cls,
         attractions: list[ Attraction ],
         *,
         month: Types.MonthInput,
         day: Types.VisitDay,
         year: Types.VisitYear,
   ) -> None:
      cls.enrich(
         attractions,
         target_date=CalendarDates.visit_target_date( month, day, year ),
      )
