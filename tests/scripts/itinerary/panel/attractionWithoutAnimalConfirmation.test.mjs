import assert from 'node:assert/strict';
import { test } from 'node:test';

import { AttractionWithoutAnimalConfirmation } from '../../../../scripts/itinerary/panel/attractionWithoutAnimalConfirmation.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_HasAttractionWithoutAnimalIssue_TestMatching_ExpectDetected', () => {
   assert.equal(
      AttractionWithoutAnimalConfirmation.hasAttractionWithoutAnimalIssue([
         { type: 'attractionWithoutAnimal' },
      ]),
      true
   );
   assert.equal(
      AttractionWithoutAnimalConfirmation.hasAttractionWithoutAnimalIssue([
         { type: 'guardiansTalkWithoutAnimal' },
      ]),
      false
   );
});

test('Test_GetPrimaryAttractionFromWithoutAnimalIssues_TestAttraction_ExpectNoTime', () => {
   assert.deepEqual(
      AttractionWithoutAnimalConfirmation.getPrimaryAttractionFromWithoutAnimalIssues([
         {
            type: 'attractionWithoutAnimal',
            items: [{ name: 'Kangaroo Walk-Thru' }],
         },
      ]),
      { attractionName: 'Kangaroo Walk-Thru' }
   );
});

test('Test_ShowAttractionWithoutAnimalConfirmation_TestMessage_ExpectNoTime', () => {
   let confirmed = false;

   AttractionWithoutAnimalConfirmation.showAttractionWithoutAnimalConfirmation({
      issues: [{
         type: 'attractionWithoutAnimal',
         items: [{ name: 'Kangaroo Walk-Thru' }],
      }],
      onConfirm: () => {
         confirmed = true;
      },
   });

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage?.textContent,
      'The Kangaroo Walk-Thru attraction does not match an animal on your itinerary. Do you still want to keep it on your plan?'
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});

test('Test_ShowAttractionWithoutAnimalConfirmation_TestMissingName_ExpectNoOp', () => {
   AttractionWithoutAnimalConfirmation.showAttractionWithoutAnimalConfirmation({
      issues: [{ type: 'attractionWithoutAnimal', items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});
