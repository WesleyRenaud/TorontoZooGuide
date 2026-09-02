from __future__ import annotations

from api.models.event import Event


EVENT_NAME = 'Conservation Carousel Ride Night'
EVENT_LOCATION = 'Front Courtyard'
EVENT_DESCRIPTION = 'Evening carousel rides for a special cause.'
EVENT_LINK = 'https://www.torontozoo.com/events/carousel-night'
EVENT_START_DATE = '2026-06-15'
EVENT_END_DATE = '2026-06-30'


def Test_ToDict_TestEventFields_ExpectFrontendShape() -> None:
   assert Event(
      name=EVENT_NAME,
      location=EVENT_LOCATION,
      description=EVENT_DESCRIPTION,
      link=EVENT_LINK,
      start_date=EVENT_START_DATE,
      end_date=EVENT_END_DATE,
   ).to_dict() == {
      'name': EVENT_NAME,
      'location': EVENT_LOCATION,
      'description': EVENT_DESCRIPTION,
      'link': EVENT_LINK,
      'start_date': EVENT_START_DATE,
      'end_date': EVENT_END_DATE,
   }
