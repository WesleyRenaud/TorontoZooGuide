from __future__ import annotations

from ..coordinators.zoo_hours_coordinator import ZooHoursCoordinator
from ...json_request_handler import JsonRequestHandler


class ZooHoursController():
   @staticmethod
   def get_zoo_hours( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      hours = ZooHoursCoordinator.get_zoo_hours(
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ) )

      handler._write_json( {
         'hours': hours.to_dict() if hours is not None else None,
      } )
