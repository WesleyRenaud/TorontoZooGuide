import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   getFixedTimeItemsFromLongWaitIssues,
   hasFixedTimeItemLongWaitIssue,
   showFixedTimeItemLongWaitConfirmation,
} from '../../scripts/itinerary/panel/fixedTimeItemLongWaitConfirmation.js';
import { updateItineraryErrorTypesFromConfig } from '../../scripts/itinerary/itineraryErrorTypes.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { MOCK_ERROR_TYPES } from './helpers/scheduleItemActionsTestSetup.mjs';

installDomTestHooks();

updateItineraryErrorTypesFromConfig({
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

const multiLongWaitIssue = {
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
};

test('hasFixedTimeItemLongWaitIssue detects matching issue type', () => {
   assert.equal(
      hasFixedTimeItemLongWaitIssue([talkLongWaitIssue]),
      true
   );
   assert.equal(
      hasFixedTimeItemLongWaitIssue([
         { type: 'guardiansTalkWithoutAnimal' },
      ]),
      false
   );
});

test('getFixedTimeItemsFromLongWaitIssues returns all named items', () => {
   assert.deepEqual(
      getFixedTimeItemsFromLongWaitIssues([
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
            typeLabel: APP_STRINGS.entityLabels.guardiansTalk,
            typePhrase: APP_STRINGS.entityPhrases.guardiansTalk,
            itemName: 'Amur Tiger',
            itemTime: '11:00 AM',
         },
         {
            issueType: 'fixedTimeItemLongWait',
            itemType: 'wildEncounter',
            typeLabel: APP_STRINGS.entityLabels.wildEncounter,
            typePhrase: APP_STRINGS.entityPhrases.wildEncounter,
            itemName: 'Capybara',
            itemTime: null,
         },
      ]
   );
});

test('getFixedTimeItemsFromLongWaitIssues rejects unsupported item types', () => {
   assert.throws(
      () => getFixedTimeItemsFromLongWaitIssues([{
         type: 'fixedTimeItemLongWait',
         items: [{
            name: 'Lunch',
            item_type: 'animal',
         }],
      }]),
      /Unsupported fixed-time long-wait item type: animal/
   );
});

test('showFixedTimeItemLongWaitConfirmation shows a single item message', () => {
   let confirmed = false;

   showFixedTimeItemLongWaitConfirmation({
      issues: [talkLongWaitIssue],
      onConfirm: () => {
         confirmed = true;
      },
   });

   assert.equal(
      document.querySelector('.itin-top-title')?.textContent,
      `Long Wait for ${APP_STRINGS.entityLabels.guardiansTalk}?`
   );
   assert.equal(
      document.querySelector('.tzg-popup-message')?.textContent,
      'The Amur Tiger guardians talk at 11:00 AM is a long wait from your other scheduled items. Do you still want to keep it on your plan?'
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});

test('showFixedTimeItemLongWaitConfirmation lists multiple items', () => {
   let confirmed = false;

   showFixedTimeItemLongWaitConfirmation({
      issues: [multiLongWaitIssue],
      onConfirm: () => {
         confirmed = true;
      },
   });

   const titles = [...document.querySelectorAll('.itin-build-warning-module-title')]
      .map((el) => el.textContent);
   const messages = [...document.querySelectorAll('.itin-build-warning-module-message')]
      .map((el) => el.textContent);

   assert.equal(
      document.querySelector('.itin-top-title')?.textContent,
      APP_STRINGS.itinerary.confirmation.saveIssuesTitle
   );
   assert.deepEqual(titles, [
      `Long Wait for ${APP_STRINGS.entityLabels.guardiansTalk}?`,
      `Long Wait for ${APP_STRINGS.entityLabels.wildEncounter}?`,
   ]);
   assert.match(messages[0], /Amur Tiger guardians talk at 11:00 AM is a long wait/);
   assert.match(messages[1], /Capybara wild encounter is a long wait/);
   assert.equal(document.querySelector('.tzg-popup-message'), null);

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});

test('showFixedTimeItemLongWaitConfirmation no-ops without named items', () => {
   showFixedTimeItemLongWaitConfirmation({
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
