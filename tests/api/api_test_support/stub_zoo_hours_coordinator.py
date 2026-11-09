from __future__ import annotations

from api_test_support.coordinator_call import CoordinatorCall

from api.models.zoo_hours import ZooHours


class StubZooHoursCoordinator():
   instances: list[ StubZooHoursCoordinator ] = []
   zoo_hours: ZooHours | None
   calls: list[ CoordinatorCall ]


   def __init__( self, *, zoo_hours: ZooHours | None ) -> None:
      self.zoo_hours = zoo_hours
      self.calls = []
      StubZooHoursCoordinator.instances.append( self )


   def get_zoo_hours(
         self,
         *,
         day: int,
         month: str,
         year: int ) -> ZooHours | None:
      self.calls.append(
         CoordinatorCall(
            'get_zoo_hours',
            {
               'day': day,
               'month': month,
               'year': year,
            },
         )
      )
      return self.zoo_hours
