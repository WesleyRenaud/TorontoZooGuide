import assert from 'node:assert/strict';
import { test } from 'node:test';

import { FixedTimeItemLongWaitConfirmation } from '../../../../scripts/itinerary/panel/fixedTimeItemLongWaitConfirmation.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { MOCK_ERROR_TYPES } from '../../helpers/scheduleItemActionsTestSetup.mjs';

installDomTestHooks();

ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
   errorTypes: MOCK_ERROR_TYPES,
   suppressedErrorTypes: [],
});

const talkLongWaitIssue = {
   type: 'fixedTimeItemLongWait',
   items: [{
      name: 'Amur Tiger',
      start_time: '11:00 AM',
      item_type: 'guardiansTalk',
   }],
};

test('Test_HasFixedTimeItemLongWaitIssue_TestMatching_ExpectDetected', () => {
   assert.equal(
      FixedTimeItemLongWaitConfirmation.hasFixedTimeItemLongWaitIssue([talkLongWaitIssue]),
      true
   );
   assert.equal(
      FixedTimeItemLongWaitConfirmation.hasFixedTimeItemLongWaitIssue([
         { type: 'guardiansTalkWithoutAnimal' },
      ]),
      false
   );
});

test('Test_GetFixedTimeItemsFromLongWaitIssues_TestNamedItems_ExpectAll', () => {
   assert.deepEqual(
      FixedTimeItemLongWaitConfirmation.getFixedTimeItemsFromLongWaitIssues([
         {
            type: 'fixedTimeItemLongWait',
            items: [
               {
                  name: '  Amur Tiger  ',
                  start_time: '11:00 AM',
                  item_type: 'guardiansTalk',
               },
               {
                  name: '   ',
                  item_type: 'guardiansTalk',
               },
               {
                  name: 'Capybara',
                  item_type: 'wildEncounter',
               },
            ],
         },
      ]),
      [
         {
            issueType: 'fixedTimeItemLongWait',
            itemType: 'guardiansTalk',
            typeLabel: Strings.entityLabels.guardiansTalk,
            typePhrase: Strings.entityPhrases.guardiansTalk,
            itemName: 'Amur Tiger',
            itemTime: '11:00 AM',
         },
         {
            issueType: 'fixedTimeItemLongWait',
            itemType: 'wildEncounter',
            typeLabel: Strings.entityLabels.wildEncounter,
            typePhrase: Strings.entityPhrases.wildEncounter,
            itemName: 'Capybara',
            itemTime: null,
         },
      ]
   );
});

test('Test_GetFixedTimeItemsFromLongWaitIssues_TestUnsupportedTypes_ExpectRejected', () => {
   assert.throws(
      () => FixedTimeItemLongWaitConfirmation.getFixedTimeItemsFromLongWaitIssues([{
         type: 'fixedTimeItemLongWait',
         items: [{
            name: 'Lunch',
            item_type: 'animal',
         }],
      }]),
      /Unsupported fixed-time long-wait item type: animal/
   );
});

test('Test_ShowFixedTimeItemLongWaitConfirmation_TestSingle_ExpectMessage', () => {
   let confirmed = false;

   FixedTimeItemLongWaitConfirmation.showFixedTimeItemLongWaitConfirmation({
      issues: [talkLongWaitIssue],
      onConfirm: () => {
         confirmed = true;
      },
   });

   assert.equal(
      document.querySelector('.itin-top-title')?.textContent,
      `Long Wait for ${Strings.entityLabels.guardiansTalk}?`
   );
   assert.equal(
      document.querySelector('.tzg-popup-message')?.textContent,
      'The Amur Tiger guardians talk at 11:00 AM is a long wait from your other scheduled items. Do you still want to keep it on your plan?'
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});

test('Test_ShowFixedTimeItemLongWaitConfirmation_TestMultiple_ExpectNoOp', () => {
   FixedTimeItemLongWaitConfirmation.showFixedTimeItemLongWaitConfirmation({
      issues: [{
         type: 'fixedTimeItemLongWait',
         items: [
            {
               name: 'Amur Tiger',
               start_time: '11:00 AM',
               item_type: 'guardiansTalk',
            },
            {
               name: 'Capybara',
               item_type: 'wildEncounter',
            },
         ],
      }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});

test('Test_ShowFixedTimeItemLongWaitConfirmation_TestUnnamed_ExpectNoOp', () => {
   FixedTimeItemLongWaitConfirmation.showFixedTimeItemLongWaitConfirmation({
      issues: [{
         type: 'fixedTimeItemLongWait',
         items: [{ name: '   ', item_type: 'guardiansTalk' }],
      }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});
