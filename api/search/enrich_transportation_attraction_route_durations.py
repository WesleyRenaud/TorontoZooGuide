from __future__ import annotations

from datetime import date

from ..itinerary.transportation.transportation_route_duration_resolver import TransportationRouteDurationResolver
from ..models import Attraction
from ..request_connection import get_connection
from ..shared.calendar_dates import CalendarDates
from ..types import MonthInput, VisitDay, VisitYear


def enrich_transportation_attraction_route_durations(
      attractions: list[ Attraction ],
      *,
      target_date: date,
) -> None:
   conn = get_connection()

   for attraction in attractions:
      if not attraction.is_also_transportation:
         continue

      attraction.route_duration_minutes = TransportationRouteDurationResolver.minutes(
         conn,
         transportation=attraction.name,
         target_date=target_date,
      )


def enrich_transportation_attraction_route_durations_for_visit(
      attractions: list[ Attraction ],
      *,
      month: MonthInput,
      day: VisitDay,
      year: VisitYear,
) -> None:
   enrich_transportation_attraction_route_durations(
      attractions,
      target_date=CalendarDates.visit_target_date( month, day, year ),
   )
