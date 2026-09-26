from __future__ import annotations

from api.models.event_site import EventSite


def Test_ToDict_TestEventSiteFields_ExpectFrontendShape() -> None:
   event_site = EventSite(
      name='Special Events Center',
      x_coord=13,
      y_coord=14 )

   result = event_site.to_dict()

   assert result[ 'name' ] == event_site.name
   assert result[ 'x_coord' ] == event_site.x_coord
   assert result[ 'y_coord' ] == event_site.y_coord
