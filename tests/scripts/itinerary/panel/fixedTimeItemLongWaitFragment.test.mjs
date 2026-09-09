import assert from 'node:assert/strict';
import { test } from 'node:test';

import { FixedTimeItemLongWaitFragment } from '../../../../scripts/itinerary/panel/fixedTimeItemLongWaitFragment.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';

installDomTestHooks();

ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
   suppressedErrorTypes: [],
});

const talkLongWaitIssue = {
   type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
   items: [{
      name: 'Amur Tiger',
      start_time: '11:00 AM',
      item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   }],
};

test('Test_HasFixedTimeItemLongWaitIssue_TestMatching_ExpectDetected', () => {
   assert.equal(
      FixedTimeItemLongWaitFragment.hasFixedTimeItemLongWaitIssue([talkLongWaitIssue]),
      true
   );
   assert.equal(
      FixedTimeItemLongWaitFragment.hasFixedTimeItemLongWaitIssue([
         { type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL },
      ]),
      false
   );
});

test('Test_GetFixedTimeItemsFromLongWaitIssues_TestNamedItems_ExpectAll', () => {
   assert.deepEqual(
      FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues([
         {
            type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
            items: [
               {
                  name: '  Amur Tiger  ',
                  start_time: '11:00 AM',
                  item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
               },
               {
                  name: '   ',
                  item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
               },
               {
                  name: 'Capybara',
                  item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
               },
            ],
         },
      ]),
      [
         {
            issueType: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
            itemType: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            typeLabel: Strings.entityLabels.guardiansTalk,
            typePhrase: Strings.entityPhrases.guardiansTalk,
            itemName: 'Amur Tiger',
            itemTime: '11:00 AM',
         },
         {
            issueType: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
            itemType: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
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
      () => FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues([{
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [{
            name: 'Lunch',
            item_type: ItinerarySaveIssueItemType.ANIMAL,
         }],
      }]),
      /Unsupported fixed-time long-wait item type: animal/
   );
});

test('Test_ShowFixedTimeItemLongWaitConfirmation_TestSingle_ExpectMessage', () => {
   let confirmed = false;

   FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation({
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
   FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation({
      issues: [{
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [
            {
               name: 'Amur Tiger',
               start_time: '11:00 AM',
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            },
            {
               name: 'Capybara',
               item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
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
   FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation({
      issues: [{
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [{ name: '   ', item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK }],
      }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});
