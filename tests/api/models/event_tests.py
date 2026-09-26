from __future__ import annotations

from api.models.event import Event


EVENT_NAME = 'Conservation Carousel Ride Night'
EVENT_LOCATION = 'Front Courtyard'
EVENT_DESCRIPTION = 'Evening carousel rides for a special cause.'
EVENT_LINK = 'https://www.torontozoo.com/events/carousel-night'
EVENT_START_DATE = '2026-06-15'
EVENT_END_DATE = '2026-06-30'


def Test_ToDict_TestEventFields_ExpectFrontendShape() -> None:
   event = Event(
      name=EVENT_NAME,
      location=EVENT_LOCATION,
      description=EVENT_DESCRIPTION,
      link=EVENT_LINK,
      start_date=EVENT_START_DATE,
      end_date=EVENT_END_DATE )

   result = event.to_dict()

   assert result[ 'name' ] == event.name
   assert result[ 'location' ] == event.location
   assert result[ 'description' ] == event.description
   assert result[ 'link' ] == event.link
   assert result[ 'start_date' ] == event.start_date
   assert result[ 'end_date' ] == event.end_date
