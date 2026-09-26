from __future__ import annotations

import pytest

from api.event_sites.coordinators.event_site_coordinator import EventSiteCoordinator
from api.event_sites.data_access.event_site_provider import EventSiteProvider
from api.models.event_site import EventSite


EVENT_SITE = EventSite( name='Waterfront Stage', x_coord=3.0, y_coord=4.0 )


def Test_GetEventSites_TestProviderRecords_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      EventSiteProvider,
      'fetch_event_sites',
      lambda _conn: [ EVENT_SITE ] )

   event_sites = EventSiteCoordinator.get_event_sites()

   assert event_sites == [ EVENT_SITE ]
