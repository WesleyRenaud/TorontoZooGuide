from __future__ import annotations

from api.models.zoo_hours import ZooHours


class StubZooHoursCoordinator():
   instances: list[ StubZooHoursCoordinator ] = []


   def __init__( self, *, zoo_hours: ZooHours | None ) -> None:
      self.zoo_hours = zoo_hours
      self.calls: list[ tuple[ str, dict[ str, object ] ] ] = []
      StubZooHoursCoordinator.instances.append( self )


   def get_zoo_hours(
         self,
         *,
         day: int,
         month: str,
         year: int ) -> ZooHours | None:
      self.calls.append(
         (
            'get_zoo_hours',
            {
               'day': day,
               'month': month,
               'year': year,
            }
         )
      )
      return self.zoo_hours
