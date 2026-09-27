import assert from 'node:assert/strict';
import { test } from 'node:test';

import { FilterDraftExcludingWarningFixedTimeItems } from '../../../../scripts/itinerary/wizard/filterDraftExcludingWarningFixedTimeItems.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';


test('Test_FilterDraftExcludingWarningFixedTimeItems_TestMatchingItems_ExpectRemoved', () => {
   const tiger = 'Amur Tiger';
   const lion = 'African Lion';
   const capybara = 'Capybara';
   const tigerTime = '11:00 AM';
   const lionTime = '2:00 PM';
   const capybaraTime = '3:00 PM';
   const draft = {
      guardiansTalks: [
         { name: tiger, start_time: tigerTime },
         { name: lion, start_time: lionTime },
      ],
      wildEncounters: [
         { name: capybara, start_time: capybaraTime },
      ],
   };
   const saveIssues = [{
      type: 'fixedTimeItemLongWait',
      items: [
         {
            name: tiger,
            start_time: tigerTime,
            item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
         },
         {
            name: capybara,
            item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
         },
      ],
   }];

   const filtered = FilterDraftExcludingWarningFixedTimeItems.filterDraftExcludingWarningFixedTimeItems(
      draft,
      saveIssues
   );

   assert.deepEqual(
      filtered.guardiansTalks.map((talk) => talk.name),
      [lion]
   );
   assert.deepEqual(filtered.wildEncounters, []);
});


test('Test_FilterDraftExcludingWarningFixedTimeItems_TestEndTimeOnly_ExpectMatched', () => {
   const kangaroo = 'Western Grey Kangaroo';
   const tortoise = 'Aldabra Tortoise';
   const kangarooTime = '11:00 AM';
   const tortoiseTime = '2:00 PM';
   const kangarooEndTime = '11:30 AM';
   const draft = {
      guardiansTalks: [
         {
            name: kangaroo,
            start_time: kangarooTime,
         },
         {
            name: tortoise,
            start_time: tortoiseTime,
         },
      ],
      wildEncounters: [],
   };
   const saveIssues = [{
      type: 'fixedTimeItemLongWait',
      items: [{
         name: kangaroo,
         item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
         start_time: kangarooTime,
         end_time: kangarooEndTime,
      }],
   }];

   const filtered = FilterDraftExcludingWarningFixedTimeItems.filterDraftExcludingWarningFixedTimeItems(
      draft,
      saveIssues
   );

   assert.deepEqual(
      filtered.guardiansTalks.map((talk) => talk.name),
      [tortoise]
   );
});


test('Test_FilterDraftExcludingWarningFixedTimeItems_TestVisitWindowOverflow_ExpectKept', () => {
   const tiger = 'Amur Tiger';
   const tigerTime = '11:00 AM';
   const draft = {
      guardiansTalks: [
         { name: tiger, start_time: tigerTime },
      ],
      wildEncounters: [],
   };
   const saveIssues = [{
      type: ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
      items: [{
         name: tiger,
         start_time: tigerTime,
         item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
      }],
   }];

   const filtered = FilterDraftExcludingWarningFixedTimeItems.filterDraftExcludingWarningFixedTimeItems(
      draft,
      saveIssues
   );

   assert.deepEqual(
      filtered.guardiansTalks.map((talk) => talk.name),
      [tiger]
   );
});
