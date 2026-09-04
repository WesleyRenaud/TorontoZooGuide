import assert from 'node:assert/strict';
import { test } from 'node:test';

import { FilterDraftExcludingWarningFixedTimeItems } from '../../../../scripts/itinerary/wizard/filterDraftExcludingWarningFixedTimeItems.js';

test('Test_FilterDraftExcludingWarningFixedTimeItems_TestMatchingItems_ExpectRemoved', () => {
   const filtered = FilterDraftExcludingWarningFixedTimeItems.filterDraftExcludingWarningFixedTimeItems(
      {
         guardiansTalks: [
            { name: 'Amur Tiger', start_time: '11:00 AM' },
            { name: 'African Lion', start_time: '2:00 PM' },
         ],
         wildEncounters: [
            { name: 'Capybara', start_time: '3:00 PM' },
         ],
      },
      [{
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
      }]
   );

   assert.deepEqual(
      filtered.guardiansTalks.map((talk) => talk.name),
      ['African Lion']
   );
   assert.deepEqual(filtered.wildEncounters, []);
});

test('Test_FilterDraftExcludingWarningFixedTimeItems_TestEndTimeOnly_ExpectMatched', () => {
   const filtered = FilterDraftExcludingWarningFixedTimeItems.filterDraftExcludingWarningFixedTimeItems(
      {
         guardiansTalks: [
            {
               name: 'Western Grey Kangaroo',
               start_time: '11:00 AM',
            },
            {
               name: 'Aldabra Tortoise',
               start_time: '2:00 PM',
            },
         ],
         wildEncounters: [],
      },
      [{
         type: 'fixedTimeItemLongWait',
         items: [{
            name: 'Western Grey Kangaroo',
            item_type: 'guardiansTalk',
            start_time: '11:00 AM',
            end_time: '11:30 AM',
         }],
      }]
   );

   assert.deepEqual(
      filtered.guardiansTalks.map((talk) => talk.name),
      ['Aldabra Tortoise']
   );
});
