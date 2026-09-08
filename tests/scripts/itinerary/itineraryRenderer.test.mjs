import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryRenderer } from '../../../scripts/itinerary/itineraryRenderer.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_GetItineraryPanelBody_TestMissingPanel_ExpectNull', () => {
   assert.equal(ItineraryRenderer.getItineraryPanelBody(), null);
});
