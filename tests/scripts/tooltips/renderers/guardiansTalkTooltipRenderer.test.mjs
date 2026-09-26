import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkLinkedAnimalOpener } from '../../../../scripts/guardians/guardiansTalkLinkedAnimalOpener.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { GuardiansTalkTooltipRenderer } from '../../../../scripts/tooltips/renderers/guardiansTalkTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateCard_TestGuardiansTalk_ExpectNamedCard', () => {
   const name = 'Amur Tiger Talk';
   const location = 'Eurasia';

   const card = GuardiansTalkTooltipRenderer.createCard({
      name,
      location,
      start_time: '11:30 AM',
      end_time: '12:00 PM',
   }, Position.FIRST);

   assert.equal(GuardiansTalkTooltipRenderer.key, 'guardiansTalk');
   assert.match(card.textContent, new RegExp(name));
   assert.match(card.textContent, new RegExp(location));
});


test('Test_CreateCard_TestLinkedAnimal_ExpectSpeciesLinkTitle', () => {
   const original = GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal;
   const name = 'Amur Tiger Talk';
   const location = 'Eurasia';
   GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal = () => ({
      species: 'Amur Tiger',
      exhibit: location,
   });

   try {
      const card = GuardiansTalkTooltipRenderer.createCard({
         name,
         location,
      }, Position.THIRD);

      assert.match(card.textContent, new RegExp(name));
      const titleLink = card.querySelector('.species-link');

      assert.equal(titleLink.textContent, name);
   } finally {
      GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal = original;
   }
});
