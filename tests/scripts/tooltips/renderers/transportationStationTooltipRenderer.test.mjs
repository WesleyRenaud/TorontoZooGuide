import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationStationTooltipRenderer } from '../../../../scripts/tooltips/renderers/transportationStationTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCard_TestStation_ExpectNamedCard', () => {
   const card = TransportationStationTooltipRenderer.createCard({
      name: 'Main Station',
      description: 'Board here',
   }, 0);
   assert.equal(TransportationStationTooltipRenderer.key, 'transportationStation');
   assert.match(card.textContent, /Main Station/);
   assert.match(card.textContent, /Board here/);
});
