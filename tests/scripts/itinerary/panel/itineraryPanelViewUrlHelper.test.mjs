import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelViewUrlHelper } from '../../../../scripts/itinerary/panel/itineraryPanelViewUrlHelper.js';

test('Test_GetDefaultLocationAndHistory_TestGlobals_ExpectSameReferences', () => {
   globalThis.location = { href: 'https://example.test' };
   globalThis.history = { replaceState() {} };

   assert.equal(ItineraryPanelViewUrlHelper.getDefaultLocation(), globalThis.location);
   assert.equal(ItineraryPanelViewUrlHelper.getDefaultHistory(), globalThis.history);
});
