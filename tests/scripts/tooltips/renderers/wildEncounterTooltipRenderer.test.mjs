import assert from 'node:assert/strict';
import test from 'node:test';

import { Position } from '../../../../scripts/shared/enums/position.js';
import { WildEncounterTooltipRenderer } from '../../../../scripts/tooltips/renderers/wildEncounterTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateCard_TestWildEncounter_ExpectNamedCard', () => {
   const name = 'Giraffe Encounter';
   const meetingSpot = 'African Savanna';

   const card = WildEncounterTooltipRenderer.createCard({
      name,
      meeting_spot: meetingSpot,
      start_time: '1:00 PM',
      end_time: '1:30 PM',
      link: 'https://example.test/giraffe',
   }, Position.FIRST);

   assert.equal(WildEncounterTooltipRenderer.key, 'wildEncounter');
   assert.match(card.textContent, new RegExp(name));
   assert.match(card.textContent, new RegExp(meetingSpot));
});
