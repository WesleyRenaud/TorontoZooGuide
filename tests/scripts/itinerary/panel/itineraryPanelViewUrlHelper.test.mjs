import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelViewUrlHelper } from '../../../../scripts/itinerary/panel/itineraryPanelViewUrlHelper.js';


test('Test_GetDefaultLocation_TestGlobalLocation_ExpectSameReference', () => {
   const location = { href: 'https://example.test' };
   globalThis.location = location;

   const defaultLocation = ItineraryPanelViewUrlHelper.getDefaultLocation();

   assert.equal(defaultLocation, location);
});


test('Test_GetDefaultHistory_TestGlobalHistory_ExpectSameReference', () => {
   const history = { replaceState() {} };
   globalThis.history = history;

   const defaultHistory = ItineraryPanelViewUrlHelper.getDefaultHistory();

   assert.equal(defaultHistory, history);
});
