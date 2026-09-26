import assert from 'node:assert/strict';
import test from 'node:test';

import { Position } from '../../../../scripts/shared/enums/position.js';
import { TransportationStationTooltipRenderer } from '../../../../scripts/tooltips/renderers/transportationStationTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateCard_TestStation_ExpectNamedCard', () => {
   const name = 'Main Station';
   const description = 'Board here';

   const card = TransportationStationTooltipRenderer.createCard({
      name,
      description,
   }, Position.FIRST);

   assert.equal(TransportationStationTooltipRenderer.key, 'transportationStation');
   assert.match(card.textContent, new RegExp(name));
   assert.match(card.textContent, new RegExp(description));
});
