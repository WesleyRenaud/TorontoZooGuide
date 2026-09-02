from __future__ import annotations

from api.models.event_site import EventSite


def Test_ToDict_TestEventSiteFields_ExpectFrontendShape() -> None:
   assert EventSite(
      name='Special Events Center',
      x_coord=13,
      y_coord=14,
   ).to_dict() == {
      'name': 'Special Events Center',
      'x_coord': 13,
      'y_coord': 14,
   }
