import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterTooltipRenderer } from '../../../../scripts/tooltips/renderers/wildEncounterTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCard_TestWildEncounter_ExpectNamedCard', () => {
   const card = WildEncounterTooltipRenderer.createCard({
      name: 'Giraffe Encounter',
      meeting_spot: 'African Savanna',
      start_time: '1:00 PM',
      end_time: '1:30 PM',
      link: 'https://example.test/giraffe',
   }, 0);

   assert.equal(WildEncounterTooltipRenderer.key, 'wildEncounter');
   assert.match(card.textContent, /Giraffe Encounter/);
   assert.match(card.textContent, /African Savanna/);
});
