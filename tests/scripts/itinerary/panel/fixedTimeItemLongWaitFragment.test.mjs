import assert from 'node:assert/strict';
import { test } from 'node:test';

import { FixedTimeItemLongWaitFragment } from '../../../../scripts/itinerary/panel/fixedTimeItemLongWaitFragment.js';
import { FixedTimeItemLongWaitMessageBuilder } from '../../../../scripts/itinerary/panel/fixedTimeItemLongWaitMessageBuilder.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
   suppressedErrorTypes: [],
});

const talkName = 'Amur Tiger';
const talkTime = '11:00 AM';
const talkLongWaitIssue = {
   type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
   items: [{
      name: talkName,
      start_time: talkTime,
      item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   }],
};


test('Test_HasFixedTimeItemLongWaitIssue_TestMatching_ExpectTrue', () => {
   const issues = [talkLongWaitIssue];

   const hasIssue = FixedTimeItemLongWaitFragment.hasFixedTimeItemLongWaitIssue(issues);

   assert.equal(hasIssue, true);
});


test('Test_HasFixedTimeItemLongWaitIssue_TestOtherType_ExpectFalse', () => {
   const issues = [{ type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL }];

   const hasIssue = FixedTimeItemLongWaitFragment.hasFixedTimeItemLongWaitIssue(issues);

   assert.equal(hasIssue, false);
});


test('Test_GetFixedTimeItemsFromLongWaitIssues_TestNamedItems_ExpectAll', () => {
   const encounterName = 'Capybara';
   const issues = [{
      type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
      items: [
         {
            name: `  ${talkName}  `,
            start_time: talkTime,
            item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
         },
         {
            name: '   ',
            item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
         },
         {
            name: encounterName,
            item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
         },
      ],
   }];

   const items = FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues(issues);

   assert.deepEqual(items, [
      {
         issueType: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         itemType: ItinerarySaveIssueItemType.GUARDIANS_TALK,
         typeLabel: Strings.entityLabels.guardiansTalk,
         typePhrase: Strings.entityPhrases.guardiansTalk,
         itemName: talkName,
         itemTime: talkTime,
      },
      {
         issueType: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         itemType: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
         typeLabel: Strings.entityLabels.wildEncounter,
         typePhrase: Strings.entityPhrases.wildEncounter,
         itemName: encounterName,
         itemTime: null,
      },
   ]);
});


test('Test_GetFixedTimeItemsFromLongWaitIssues_TestUnsupportedTypes_ExpectRejected', () => {
   const issues = [{
      type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
      items: [{
         name: 'Lunch',
         item_type: ItinerarySaveIssueItemType.ANIMAL,
      }],
   }];

   assert.throws(
      () => FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues(issues),
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

   const items = FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues([talkLongWaitIssue]);
   const item = items.at(Position.FIRST);
   const title = document.querySelector('.itin-top-title');
   const message = document.querySelector('.tzg-popup-message');

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(
      title?.textContent,
      Strings.itinerary.confirmation.fixedTimeItemLongWaitTitle(item.typeLabel)
   );
   assert.equal(
      message?.textContent,
      FixedTimeItemLongWaitMessageBuilder.longWaitConfirmMessage(item, Strings.itinerary.confirmation)
   );
   assert.equal(confirmed, true);
});


test('Test_ShowFixedTimeItemLongWaitConfirmation_TestMultiple_ExpectNoOp', () => {
   FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation({
      issues: [{
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [
            {
               name: talkName,
               start_time: talkTime,
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

   const popup = document.querySelector('.tzg-popup');

   assert.equal(popup, null);
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

   const popup = document.querySelector('.tzg-popup');

   assert.equal(popup, null);
});
