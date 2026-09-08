import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionSelectorRendererHelper } from '../../../../../scripts/itinerary/selectors/regionSelector/regionSelectorRendererHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEmptyState_TestMessage_ExpectEmptyElement', () => {
   const emptyEl = RegionSelectorRendererHelper.createEmptyState('No regions');
   assert.equal(emptyEl.className, 'itin-empty');
   assert.equal(emptyEl.textContent, 'No regions');
});
