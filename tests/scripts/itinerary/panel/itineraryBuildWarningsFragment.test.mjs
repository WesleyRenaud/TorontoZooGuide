import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryBuildWarningsFragment } from '../../../../scripts/itinerary/panel/itineraryBuildWarningsFragment.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';

installDomTestHooks();

ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
   suppressedErrorTypes: [],
});

const overlapAndWithoutAnimalIssues = [
   {
      type: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      items: [{
         name: 'Amur Tiger',
         start_time: '11:00 AM',
      }],
   },
   {
      type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      items: [{
         name: 'Amur Tiger',
         start_time: '11:00 AM',
      }],
   },
];

test('Test_HasMultipleItineraryBuildWarnings_TestHasMultipleItineraryBuildWarningsDetectsMultipleWarningTypes_ExpectOk', () => {
   assert.equal(
      ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings(overlapAndWithoutAnimalIssues),
      true
   );
   assert.equal(
      ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings([
         overlapAndWithoutAnimalIssues[0],
      ]),
      false
   );
});

test('Test_HasMultipleItineraryBuildWarnings_TestHasMultipleItineraryBuildWarningsDetectsMultipleLongWaitItems_ExpectOk', () => {
   assert.equal(
      ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings([{
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [
            {
               name: 'Western Grey Kangaroo',
               start_time: '11:00 AM',
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            },
            {
               name: 'Aldabra Tortoise',
               start_time: '2:00 PM',
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            },
         ],
      }]),
      true
   );
   assert.equal(
      ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings([{
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [{
            name: 'Western Grey Kangaroo',
            start_time: '11:00 AM',
            item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
         }],
      }]),
      false
   );
});

test('Test_HasMultipleItineraryBuildWarnings_TestHasMultipleItineraryBuildWarningsDetectsMultipleWithoutAnimalTalks_ExpectOk', () => {
   assert.equal(
      ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings([{
         type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
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
      ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings(overlapAndWithoutAnimalIssues),
      {
         confirmingGuardiansTalkUnschedule: true,
         confirmingGuardiansTalkWithoutAnimal: true,
      }
   );
});

test('Test_BuildItineraryBuildWarningSections_TestBuildItineraryBuildWarningSectionsIncludesEachWarningMessage_ExpectOk', () => {
   const sections = ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections(
      overlapAndWithoutAnimalIssues
   );

   assert.equal(sections.length, 2);
   assert.equal(sections[0].type, ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS);
   assert.equal(sections[0].title, 'Schedule overlap');
   assert.match(sections[0].message, /Amur Tiger/);
   assert.equal(sections[1].type, ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL);
   assert.equal(sections[1].title, 'No matching animal');
   assert.match(sections[1].message, /does not match an animal/);
});

test('Test_BuildItineraryBuildWarningSections_TestBuildItineraryBuildWarningSectionsCoversEncounterAndNoTimeCopy_ExpectOk', () => {
   const sections = ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections([
      {
         type: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         items: [{ name: 'Capybara' }],
      },
      {
         type: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         items: [{ name: 'Amur Tiger' }],
      },
      {
         type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
         items: [{ name: 'Amur Tiger' }],
      },
      {
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [
            {
               name: 'Amur Tiger',
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            },
            {
               name: 'Indian Rhino',
               start_time: '1:00 PM',
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            },
            {
               name: 'Capybara',
               item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
            },
         ],
      },
   ]);

   assert.deepEqual(
      sections.map((section) => section.type),
      [
         ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
         ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
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

   ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation({
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

   ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation({
      issues: [{
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [
            {
               name: 'Western Grey Kangaroo',
               start_time: '11:00 AM',
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            },
            {
               name: 'Aldabra Tortoise',
               start_time: '2:00 PM',
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
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
   ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation({
      issues: [
         {
            type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
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
            type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
            items: [
               {
                  name: 'Western Grey Kangaroo',
                  start_time: '11:00 AM',
                  item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
               },
               {
                  name: 'African Lion',
                  start_time: '2:00 PM',
                  item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
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
   const sections = ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections([
      {
         type: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
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
      ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections([
         { type: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS, items: [] },
         { type: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS, items: [] },
         { type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL, items: [] },
         { type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT, items: [] },
      ]),
      []
   );
});

test('Test_ShowItineraryBuildWarningsConfirmation_TestShowItineraryBuildWarningsConfirmationCancelsWhenNoSections_ExpectOk', () => {
   let cancelled = false;

   ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation({
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
