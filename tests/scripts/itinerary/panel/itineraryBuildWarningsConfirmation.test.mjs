import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryBuildWarningsConfirmation } from '../../../../scripts/itinerary/panel/itineraryBuildWarningsConfirmation.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { MOCK_ERROR_TYPES } from '../../helpers/scheduleItemActionsTestSetup.mjs';

installDomTestHooks();

ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
   errorTypes: MOCK_ERROR_TYPES,
   suppressedErrorTypes: [],
});

const overlapAndWithoutAnimalIssues = [
   {
      type: 'guardiansTalkWillUnscheduleItems',
      items: [{
         name: 'Amur Tiger',
         start_time: '11:00 AM',
      }],
   },
   {
      type: 'guardiansTalkWithoutAnimal',
      items: [{
         name: 'Amur Tiger',
         start_time: '11:00 AM',
      }],
   },
];

test('Test_HasMultipleItineraryBuildWarnings_TestHasMultipleItineraryBuildWarningsDetectsMultipleWarningTypes_ExpectOk', () => {
   assert.equal(
      ItineraryBuildWarningsConfirmation.hasMultipleItineraryBuildWarnings(overlapAndWithoutAnimalIssues),
      true
   );
   assert.equal(
      ItineraryBuildWarningsConfirmation.hasMultipleItineraryBuildWarnings([
         overlapAndWithoutAnimalIssues[0],
      ]),
      false
   );
});

test('Test_HasMultipleItineraryBuildWarnings_TestHasMultipleItineraryBuildWarningsDetectsMultipleLongWaitItems_ExpectOk', () => {
   assert.equal(
      ItineraryBuildWarningsConfirmation.hasMultipleItineraryBuildWarnings([{
         type: 'fixedTimeItemLongWait',
         items: [
            {
               name: 'Western Grey Kangaroo',
               start_time: '11:00 AM',
               item_type: 'guardiansTalk',
            },
            {
               name: 'Aldabra Tortoise',
               start_time: '2:00 PM',
               item_type: 'guardiansTalk',
            },
         ],
      }]),
      true
   );
   assert.equal(
      ItineraryBuildWarningsConfirmation.hasMultipleItineraryBuildWarnings([{
         type: 'fixedTimeItemLongWait',
         items: [{
            name: 'Western Grey Kangaroo',
            start_time: '11:00 AM',
            item_type: 'guardiansTalk',
         }],
      }]),
      false
   );
});

test('Test_HasMultipleItineraryBuildWarnings_TestHasMultipleItineraryBuildWarningsDetectsMultipleWithoutAnimalTalks_ExpectOk', () => {
   assert.equal(
      ItineraryBuildWarningsConfirmation.hasMultipleItineraryBuildWarnings([{
         type: 'guardiansTalkWithoutAnimal',
         items: [
            {
               name: 'Western Grey Kangaroo',
               start_time: '11:00 AM',
            },
            {
               name: 'African Lion',
               start_time: '2:00 PM',
            },
         ],
      }]),
      true
   );
});

test('Test_BuildConfirmedOptionsFromBuildWarnings_TestBuildConfirmedOptionsFromBuildWarningsSetsAllMatchingFlags_ExpectOk', () => {
   assert.deepEqual(
      ItineraryBuildWarningsConfirmation.buildConfirmedOptionsFromBuildWarnings(overlapAndWithoutAnimalIssues),
      {
         confirmingGuardiansTalkUnschedule: true,
         confirmingGuardiansTalkWithoutAnimal: true,
      }
   );
});

test('Test_BuildItineraryBuildWarningSections_TestBuildItineraryBuildWarningSectionsIncludesEachWarningMessage_ExpectOk', () => {
   const sections = ItineraryBuildWarningsConfirmation.buildItineraryBuildWarningSections(
      overlapAndWithoutAnimalIssues
   );

   assert.equal(sections.length, 2);
   assert.equal(sections[0].type, 'guardiansTalkWillUnscheduleItems');
   assert.equal(sections[0].title, 'Schedule overlap');
   assert.match(sections[0].message, /Amur Tiger/);
   assert.equal(sections[1].type, 'guardiansTalkWithoutAnimal');
   assert.equal(sections[1].title, 'No matching animal');
   assert.match(sections[1].message, /does not match an animal/);
});

test('Test_BuildItineraryBuildWarningSections_TestBuildItineraryBuildWarningSectionsCoversEncounterAndNoTimeCopy_ExpectOk', () => {
   const sections = ItineraryBuildWarningsConfirmation.buildItineraryBuildWarningSections([
      {
         type: 'wildEncounterWillUnscheduleItems',
         items: [{ name: 'Capybara' }],
      },
      {
         type: 'guardiansTalkWillUnscheduleItems',
         items: [{ name: 'Amur Tiger' }],
      },
      {
         type: 'guardiansTalkWithoutAnimal',
         items: [{ name: 'Amur Tiger' }],
      },
      {
         type: 'fixedTimeItemLongWait',
         items: [
            {
               name: 'Amur Tiger',
               item_type: 'guardiansTalk',
            },
            {
               name: 'Indian Rhino',
               start_time: '1:00 PM',
               item_type: 'guardiansTalk',
            },
            {
               name: 'Capybara',
               item_type: 'wildEncounter',
            },
         ],
      },
   ]);

   assert.deepEqual(
      sections.map((section) => section.type),
      [
         'guardiansTalkWillUnscheduleItems',
         'wildEncounterWillUnscheduleItems',
         'guardiansTalkWithoutAnimal',
         'fixedTimeItemLongWait',
         'fixedTimeItemLongWait',
         'fixedTimeItemLongWait',
      ]
   );
   assert.match(sections[0].message, /Amur Tiger guardians talk overlaps/);
   assert.match(sections[1].message, /Capybara wild encounter overlaps/);
   assert.match(sections[2].message, /does not match an animal on your itinerary\.$/);
   assert.match(sections[3].message, /Amur Tiger guardians talk is a long wait/);
   assert.match(sections[4].message, /Indian Rhino guardians talk at 1:00 PM is a long wait/);
   assert.match(sections[5].message, /Capybara wild encounter is a long wait/);
});

test('Test_ShowItineraryBuildWarningsConfirmation_TestShowItineraryBuildWarningsConfirmationShowsAllWarningsInOnePopup_ExpectOk', () => {
   let confirmed = false;

   ItineraryBuildWarningsConfirmation.showItineraryBuildWarningsConfirmation({
      issues: overlapAndWithoutAnimalIssues,
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
      'Your Itinerary Has the Following Issues:'
   );
   assert.equal(
      document.querySelectorAll('.itin-build-warning-module').length,
      2
   );
   assert.deepEqual(titles, [
      'Schedule overlap',
      'No matching animal',
   ]);
   assert.equal(messages.length, 2);
   assert.doesNotMatch(messages.join(' '), /\?/);

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});

test('Test_ShowItineraryBuildWarningsConfirmation_TestShowItineraryBuildWarningsConfirmationListsMultipleLongWaitItems_ExpectOk', () => {
   let confirmed = false;

   ItineraryBuildWarningsConfirmation.showItineraryBuildWarningsConfirmation({
      issues: [{
         type: 'fixedTimeItemLongWait',
         items: [
            {
               name: 'Western Grey Kangaroo',
               start_time: '11:00 AM',
               item_type: 'guardiansTalk',
            },
            {
               name: 'Aldabra Tortoise',
               start_time: '2:00 PM',
               item_type: 'guardiansTalk',
            },
         ],
      }],
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
      'Your Itinerary Has the Following Issues:'
   );
   assert.deepEqual(titles, ['Long wait', 'Long wait']);
   assert.match(
      messages[0],
      /Western Grey Kangaroo guardians talk at 11:00 AM is a long wait/
   );
   assert.match(
      messages[1],
      /Aldabra Tortoise guardians talk at 2:00 PM is a long wait/
   );
   assert.doesNotMatch(messages.join(' '), /\?/);
   assert.equal(document.querySelector('.tzg-popup-message'), null);

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});

test('Test_ShowItineraryBuildWarningsConfirmation_TestShowItineraryBuildWarningsConfirmationListsEachWithoutAnimalTalk_ExpectOk', () => {
   ItineraryBuildWarningsConfirmation.showItineraryBuildWarningsConfirmation({
      issues: [
         {
            type: 'guardiansTalkWithoutAnimal',
            items: [
               {
                  name: 'Western Grey Kangaroo',
                  start_time: '11:00 AM',
               },
               {
                  name: 'African Lion',
                  start_time: '2:00 PM',
               },
            ],
         },
         {
            type: 'fixedTimeItemLongWait',
            items: [
               {
                  name: 'Western Grey Kangaroo',
                  start_time: '11:00 AM',
                  item_type: 'guardiansTalk',
               },
               {
                  name: 'African Lion',
                  start_time: '2:00 PM',
                  item_type: 'guardiansTalk',
               },
            ],
         },
      ],
   });

   const titles = [...document.querySelectorAll('.itin-build-warning-module-title')]
      .map((el) => el.textContent);
   const messages = [...document.querySelectorAll('.itin-build-warning-module-message')]
      .map((el) => el.textContent);

   assert.deepEqual(titles, [
      'No matching animal',
      'No matching animal',
      'Long wait',
      'Long wait',
   ]);
   assert.match(messages[0], /Western Grey Kangaroo guardians talk at 11:00 AM/);
   assert.match(messages[1], /African Lion guardians talk at 2:00 PM/);
   assert.match(messages[2], /Western Grey Kangaroo guardians talk at 11:00 AM is a long wait/);
   assert.match(messages[3], /African Lion guardians talk at 2:00 PM is a long wait/);
});

test('Test_BuildItineraryBuildWarningSections_TestBuildItineraryBuildWarningSectionsCoversTimedWildEncounterOverlapCopy_ExpectOk', () => {
   const sections = ItineraryBuildWarningsConfirmation.buildItineraryBuildWarningSections([
      {
         type: 'wildEncounterWillUnscheduleItems',
         items: [{
            name: 'Capybara',
            start_time: '2:30 PM',
         }],
      },
   ]);

   assert.equal(sections.length, 1);
   assert.match(
      sections[0].message,
      /Capybara wild encounter at 2:30 PM overlaps scheduled items/
   );
});

test('Test_BuildItineraryBuildWarningSections_TestBuildItineraryBuildWarningSectionsSkipsEmptyWarningModules_ExpectOk', () => {
   assert.deepEqual(
      ItineraryBuildWarningsConfirmation.buildItineraryBuildWarningSections([
         { type: 'guardiansTalkWillUnscheduleItems', items: [] },
         { type: 'wildEncounterWillUnscheduleItems', items: [] },
         { type: 'guardiansTalkWithoutAnimal', items: [] },
         { type: 'fixedTimeItemLongWait', items: [] },
      ]),
      []
   );
});

test('Test_BuildItineraryBuildWarningSections_TestBuildItineraryBuildWarningSectionsSkipsLongWaitWhenErrorTypeIs_ExpectOk', () => {
   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
      errorTypes: {
         ...MOCK_ERROR_TYPES,
         FIXED_TIME_ITEM_LONG_WAIT: '',
      },
      suppressedErrorTypes: [],
   });

   try {
      assert.deepEqual(
         ItineraryBuildWarningsConfirmation.buildItineraryBuildWarningSections([{
            type: 'fixedTimeItemLongWait',
            items: [{
               name: 'Amur Tiger',
               item_type: 'guardiansTalk',
            }],
         }]),
         []
      );
   }
   finally {
      ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
         errorTypes: MOCK_ERROR_TYPES,
         suppressedErrorTypes: [],
      });
   }
});

test('Test_ShowItineraryBuildWarningsConfirmation_TestShowItineraryBuildWarningsConfirmationCancelsWhenNoSections_ExpectOk', () => {
   let cancelled = false;

   ItineraryBuildWarningsConfirmation.showItineraryBuildWarningsConfirmation({
      issues: [],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
      onCancel: () => {
         cancelled = true;
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
   assert.equal(cancelled, true);
});
