import assert from 'node:assert/strict';
import { test } from 'node:test';

import { AttractionWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/attractionWithoutAnimalFragment.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_HasAttractionWithoutAnimalIssue_TestMatching_ExpectDetected', () => {
   assert.equal(
      AttractionWithoutAnimalFragment.hasAttractionWithoutAnimalIssue([
         { type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL },
      ]),
      true
   );
   assert.equal(
      AttractionWithoutAnimalFragment.hasAttractionWithoutAnimalIssue([
         { type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL },
      ]),
      false
   );
});

test('Test_GetPrimaryAttractionFromWithoutAnimalIssues_TestAttraction_ExpectNoTime', () => {
   assert.deepEqual(
      AttractionWithoutAnimalFragment.getPrimaryAttractionFromWithoutAnimalIssues([
         {
            type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
            items: [{ name: 'Kangaroo Walk-Thru' }],
         },
      ]),
      { attractionName: 'Kangaroo Walk-Thru' }
   );
});

test('Test_ShowAttractionWithoutAnimalConfirmation_TestMessage_ExpectNoTime', () => {
   let confirmed = false;

   AttractionWithoutAnimalFragment.showAttractionWithoutAnimalConfirmation({
      issues: [{
         type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
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
   AttractionWithoutAnimalFragment.showAttractionWithoutAnimalConfirmation({
      issues: [{ type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL, items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});

test('Test_GetAttractionNamesFromWithoutAnimalIssues_TestNamesTimesAndBlanks_ExpectFiltered', () => {
   assert.deepEqual(
      AttractionWithoutAnimalFragment.getAttractionNamesFromWithoutAnimalIssues([{
         type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
         items: [
            { name: '  Kangaroo Walk-Thru  ', start_time: '11:00' },
            { name: '   ' },
            { name: 'Splash Island', start_time: '2:00 PM' },
         ],
      }]),
      ['Kangaroo Walk-Thru', 'Splash Island']
   );

   assert.match(
      AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage({
         attractionName: 'Splash Island',
         attractionTime: '2:00 PM',
      }),
      /Splash Island.*2:00 PM/
   );
});
