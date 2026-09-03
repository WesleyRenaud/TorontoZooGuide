import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   getPrimaryAttractionFromWithoutAnimalIssues,
   hasAttractionWithoutAnimalIssue,
   showAttractionWithoutAnimalConfirmation,
} from '../../scripts/itinerary/panel/attractionWithoutAnimalConfirmation.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

installDomTestHooks();

test('hasAttractionWithoutAnimalIssue detects matching issue type', () => {
   assert.equal(
      hasAttractionWithoutAnimalIssue([
         { type: 'attractionWithoutAnimal' },
      ]),
      true
   );
   assert.equal(
      hasAttractionWithoutAnimalIssue([
         { type: 'guardiansTalkWithoutAnimal' },
      ]),
      false
   );
});

test('getPrimaryAttractionFromWithoutAnimalIssues returns attraction without time', () => {
   assert.deepEqual(
      getPrimaryAttractionFromWithoutAnimalIssues([
         {
            type: 'attractionWithoutAnimal',
            items: [{ name: 'Kangaroo Walk-Thru' }],
         },
      ]),
      { attractionName: 'Kangaroo Walk-Thru' }
   );
});

test('showAttractionWithoutAnimalConfirmation uses message without time', () => {
   let confirmed = false;

   showAttractionWithoutAnimalConfirmation({
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

test('showAttractionWithoutAnimalConfirmation no-ops without attraction name', () => {
   showAttractionWithoutAnimalConfirmation({
      issues: [{ type: 'attractionWithoutAnimal', items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});
