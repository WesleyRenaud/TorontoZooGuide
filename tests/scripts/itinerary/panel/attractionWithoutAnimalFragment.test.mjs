import assert from 'node:assert/strict';
import { test } from 'node:test';

import { AttractionWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/attractionWithoutAnimalFragment.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_HasAttractionWithoutAnimalIssue_TestMatching_ExpectTrue', () => {
   const issues = [{ type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL }];

   const hasIssue = AttractionWithoutAnimalFragment.hasAttractionWithoutAnimalIssue(issues);

   assert.equal(hasIssue, true);
});


test('Test_HasAttractionWithoutAnimalIssue_TestOtherType_ExpectFalse', () => {
   const issues = [{ type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL }];

   const hasIssue = AttractionWithoutAnimalFragment.hasAttractionWithoutAnimalIssue(issues);

   assert.equal(hasIssue, false);
});


test('Test_GetPrimaryAttractionFromWithoutAnimalIssues_TestAttraction_ExpectNoTime', () => {
   const attractionName = 'Kangaroo Walk-Thru';
   const issues = [{
      type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
      items: [{ name: attractionName }],
   }];

   const attraction = AttractionWithoutAnimalFragment.getPrimaryAttractionFromWithoutAnimalIssues(issues);

   assert.deepEqual(attraction, { attractionName });
});


test('Test_ShowAttractionWithoutAnimalConfirmation_TestMessage_ExpectNoTime', () => {
   const attractionName = 'Kangaroo Walk-Thru';
   let confirmed = false;

   AttractionWithoutAnimalFragment.showAttractionWithoutAnimalConfirmation({
      issues: [{
         type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
         items: [{ name: attractionName }],
      }],
      onConfirm: () => {
         confirmed = true;
      },
   });

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage?.textContent,
      AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_CONFIG.getMessageWithoutTime(
         attractionName
      )
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

   const popup = document.querySelector('.tzg-popup');

   assert.equal(popup, null);
});


test('Test_GetAttractionNamesFromWithoutAnimalIssues_TestNamesTimesAndBlanks_ExpectFiltered', () => {
   const kangaroo = 'Kangaroo Walk-Thru';
   const splashIsland = 'Splash Island';
   const issues = [{
      type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
      items: [
         { name: `  ${kangaroo}  `, start_time: '11:00' },
         { name: '   ' },
         { name: splashIsland, start_time: '2:00 PM' },
      ],
   }];

   const names = AttractionWithoutAnimalFragment.getAttractionNamesFromWithoutAnimalIssues(issues);

   assert.deepEqual(names, [kangaroo, splashIsland]);
});


test('Test_GetAttractionsFromWithoutAnimalIssues_TestNamedItems_ExpectAttractions', () => {
   const splashIsland = 'Splash Island';
   const splashTime = '2:00 PM';
   const kangaroo = 'Kangaroo Walk-Thru';
   const issues = [{
      type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
      items: [
         { name: splashIsland, start_time: splashTime },
         { name: kangaroo },
      ],
   }];

   const attractions = AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues(issues);

   assert.deepEqual(attractions, [
      { attractionName: splashIsland, attractionTime: splashTime },
      { attractionName: kangaroo },
   ]);
});


test('Test_AttractionWithoutAnimalMessage_TestWithTime_ExpectMessage', () => {
   const attractionName = 'Splash Island';
   const attractionTime = '2:00 PM';

   const message = AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage({
      attractionName,
      attractionTime,
   });

   assert.match(message, new RegExp(attractionName));
   assert.match(message, new RegExp(attractionTime.replace(':', '\\:')));
});


test('Test_ShowAttractionWithoutAnimalConfirmation_TestMessage_ExpectWithTime', () => {
   const attractionName = 'Splash Island';
   const attractionTime = '2:00 PM';

   AttractionWithoutAnimalFragment.showAttractionWithoutAnimalConfirmation({
      issues: [{
         type: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
         items: [{ name: attractionName, start_time: attractionTime }],
      }],
      onConfirm: () => {},
   });

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage?.textContent,
      AttractionWithoutAnimalFragment.ATTRACTION_WITHOUT_ANIMAL_CONFIG.getMessage(
         attractionName,
         attractionTime
      )
   );
});
