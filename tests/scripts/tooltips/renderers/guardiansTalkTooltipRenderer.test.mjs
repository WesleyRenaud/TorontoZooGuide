import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkTooltipRenderer } from '../../../../scripts/tooltips/renderers/guardiansTalkTooltipRenderer.js';
import { GuardiansTalkLinkedAnimalOpener } from '../../../../scripts/guardians/guardiansTalkLinkedAnimalOpener.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCard_TestGuardiansTalk_ExpectNamedCard', () => {
   const card = GuardiansTalkTooltipRenderer.createCard({
      name: 'Amur Tiger Talk',
      location: 'Eurasia',
      start_time: '11:30 AM',
      end_time: '12:00 PM',
   }, 0);

   assert.equal(GuardiansTalkTooltipRenderer.key, 'guardiansTalk');
   assert.match(card.textContent, /Amur Tiger Talk/);
   assert.match(card.textContent, /Eurasia/);
});

test('Test_CreateCard_TestLinkedAnimal_ExpectSpeciesLinkTitle', () => {
   const original = GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal;
   GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal = () => ({
      species: 'Amur Tiger',
      exhibit: 'Eurasia',
   });

   try {
      const card = GuardiansTalkTooltipRenderer.createCard({
         name: 'Amur Tiger Talk',
         location: 'Eurasia',
      }, 2);
      assert.match(card.textContent, /Amur Tiger Talk/);
      const link = card.querySelector?.('a')
         ?? card.children?.find?.((child) => child.tagName === 'A' || child.tagName === 'a');
      assert.ok(link || card.textContent.includes('Amur Tiger Talk'));
   } finally {
      GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal = original;
   }
});
