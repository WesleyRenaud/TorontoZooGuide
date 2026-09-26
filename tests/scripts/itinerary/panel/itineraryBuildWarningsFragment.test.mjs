import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryBuildWarningsFragment } from '../../../../scripts/itinerary/panel/itineraryBuildWarningsFragment.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
   suppressedErrorTypes: [],
});

const talkName = 'Amur Tiger';
const talkTime = '11:00 AM';
const overlapAndWithoutAnimalIssues = [
   {
      type: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      items: [{
         name: talkName,
         start_time: talkTime,
      }],
   },
   {
      type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      items: [{
         name: talkName,
         start_time: talkTime,
      }],
   },
];

installDomTestHooks();


test('Test_HasMultipleItineraryBuildWarnings_TestMultipleWarningTypes_ExpectTrue', () => {
   const hasMultiple = ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings(
      overlapAndWithoutAnimalIssues
   );

   assert.equal(hasMultiple, true);
});


test('Test_HasMultipleItineraryBuildWarnings_TestSingleWarningType_ExpectFalse', () => {
   const issues = [overlapAndWithoutAnimalIssues.at(Position.FIRST)];

   const hasMultiple = ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings(issues);

   assert.equal(hasMultiple, false);
});


test('Test_HasMultipleItineraryBuildWarnings_TestMultipleLongWaitItems_ExpectTrue', () => {
   const issues = [{
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
   }];

   const hasMultiple = ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings(issues);

   assert.equal(hasMultiple, true);
});


test('Test_HasMultipleItineraryBuildWarnings_TestSingleLongWaitItem_ExpectFalse', () => {
   const issues = [{
      type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
      items: [{
         name: 'Western Grey Kangaroo',
         start_time: '11:00 AM',
         item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
      }],
   }];

   const hasMultiple = ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings(issues);

   assert.equal(hasMultiple, false);
});


test('Test_HasMultipleItineraryBuildWarnings_TestMultipleWithoutAnimalTalks_ExpectTrue', () => {
   const issues = [{
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
   }];

   const hasMultiple = ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings(issues);

   assert.equal(hasMultiple, true);
});


test('Test_BuildConfirmedOptionsFromBuildWarnings_TestMatchingFlags_ExpectSet', () => {
   const options = ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings(
      overlapAndWithoutAnimalIssues
   );

   assert.deepEqual(options, {
      confirmingGuardiansTalkUnschedule: true,
      confirmingGuardiansTalkWithoutAnimal: true,
   });
});


test('Test_BuildItineraryBuildWarningSections_TestOverlapAndWithoutAnimal_ExpectMessages', () => {
   const sections = ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections(
      overlapAndWithoutAnimalIssues
   );
   const overlap = sections.at(Position.FIRST);
   const withoutAnimal = sections.at(Position.SECOND);

   assert.equal(sections.length, Position.THIRD);
   assert.equal(overlap.type, ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS);
   assert.equal(overlap.title, Strings.itinerary.confirmation.buildWarningScheduleOverlapTitle);
   assert.equal(
      overlap.message,
      Strings.itinerary.confirmation.buildWarningScheduleOverlapMessage(talkName, talkTime)
   );
   assert.equal(withoutAnimal.type, ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL);
   assert.equal(withoutAnimal.title, Strings.itinerary.confirmation.buildWarningWithoutAnimalTitle);
   assert.equal(
      withoutAnimal.message,
      Strings.itinerary.confirmation.buildWarningWithoutAnimalMessage(talkName, talkTime)
   );
});


test('Test_BuildItineraryBuildWarningSections_TestEncounterAndNoTimeCopy_ExpectSections', () => {
   const encounterName = 'Capybara';
   const rhinoName = 'Indian Rhino';
   const rhinoTime = '1:00 PM';
   const issues = [
      {
         type: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         items: [{ name: encounterName }],
      },
      {
         type: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         items: [{ name: talkName }],
      },
      {
         type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
         items: [{ name: talkName }],
      },
      {
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [
            {
               name: talkName,
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            },
            {
               name: rhinoName,
               start_time: rhinoTime,
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            },
            {
               name: encounterName,
               item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
            },
         ],
      },
   ];

   const sections = ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections(issues);

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
   assert.equal(
      sections.at(Position.FIRST).message,
      Strings.itinerary.confirmation.buildWarningScheduleOverlapMessageWithoutTime(talkName)
   );
   assert.equal(
      sections.at(Position.SECOND).message,
      Strings.itinerary.confirmation.buildWarningWildEncounterOverlapMessageWithoutTime(encounterName)
   );
   assert.equal(
      sections.at(Position.THIRD).message,
      Strings.itinerary.confirmation.buildWarningWithoutAnimalMessageWithoutTime(talkName)
   );
   assert.equal(
      sections.at(Position.FOURTH).message,
      Strings.itinerary.confirmation.buildWarningLongWaitMessageWithoutTime(
         talkName,
         Strings.entityPhrases.guardiansTalk
      )
   );
   assert.equal(
      sections[4].message,
      Strings.itinerary.confirmation.buildWarningLongWaitMessage(
         rhinoName,
         rhinoTime,
         Strings.entityPhrases.guardiansTalk
      )
   );
   assert.equal(
      sections[5].message,
      Strings.itinerary.confirmation.buildWarningLongWaitMessageWithoutTime(
         encounterName,
         Strings.entityPhrases.wildEncounter
      )
   );
});


test('Test_ShowItineraryBuildWarningsConfirmation_TestMultipleWarnings_ExpectOnePopup', () => {
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
   const popupTitle = document.querySelector('.itin-top-title')?.textContent;
   const modules = document.querySelectorAll('.itin-build-warning-module');

   assert.equal(popupTitle, Strings.itinerary.confirmation.saveIssuesTitle);
   assert.equal(modules.length, Position.THIRD);
   assert.deepEqual(titles, [
      Strings.itinerary.confirmation.buildWarningScheduleOverlapTitle,
      Strings.itinerary.confirmation.buildWarningWithoutAnimalTitle,
   ]);
   assert.equal(messages.length, Position.THIRD);
   assert.doesNotMatch(messages.join(' '), /\?/);

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});


test('Test_ShowItineraryBuildWarningsConfirmation_TestMultipleLongWaitItems_ExpectListed', () => {
   const kangarooName = 'Western Grey Kangaroo';
   const kangarooTime = '11:00 AM';
   const tortoiseName = 'Aldabra Tortoise';
   const tortoiseTime = '2:00 PM';
   let confirmed = false;

   ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation({
      issues: [{
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [
            {
               name: kangarooName,
               start_time: kangarooTime,
               item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
            },
            {
               name: tortoiseName,
               start_time: tortoiseTime,
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
   const popupTitle = document.querySelector('.itin-top-title')?.textContent;

   assert.equal(popupTitle, Strings.itinerary.confirmation.saveIssuesTitle);
   assert.deepEqual(titles, [
      Strings.itinerary.confirmation.buildWarningLongWaitTitle,
      Strings.itinerary.confirmation.buildWarningLongWaitTitle,
   ]);
   assert.equal(
      messages.at(Position.FIRST),
      Strings.itinerary.confirmation.buildWarningLongWaitMessage(
         kangarooName,
         kangarooTime,
         Strings.entityPhrases.guardiansTalk
      )
   );
   assert.equal(
      messages.at(Position.SECOND),
      Strings.itinerary.confirmation.buildWarningLongWaitMessage(
         tortoiseName,
         tortoiseTime,
         Strings.entityPhrases.guardiansTalk
      )
   );
   assert.doesNotMatch(messages.join(' '), /\?/);
   assert.equal(document.querySelector('.tzg-popup-message'), null);

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});


test('Test_ShowItineraryBuildWarningsConfirmation_TestWithoutAnimalAndLongWait_ExpectListed', () => {
   const kangarooName = 'Western Grey Kangaroo';
   const kangarooTime = '11:00 AM';
   const lionName = 'African Lion';
   const lionTime = '2:00 PM';

   ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation({
      issues: [
         {
            type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
            items: [
               {
                  name: kangarooName,
                  start_time: kangarooTime,
               },
               {
                  name: lionName,
                  start_time: lionTime,
               },
            ],
         },
         {
            type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
            items: [
               {
                  name: kangarooName,
                  start_time: kangarooTime,
                  item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
               },
               {
                  name: lionName,
                  start_time: lionTime,
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
      Strings.itinerary.confirmation.buildWarningWithoutAnimalTitle,
      Strings.itinerary.confirmation.buildWarningWithoutAnimalTitle,
      Strings.itinerary.confirmation.buildWarningLongWaitTitle,
      Strings.itinerary.confirmation.buildWarningLongWaitTitle,
   ]);
   assert.equal(
      messages.at(Position.FIRST),
      Strings.itinerary.confirmation.buildWarningWithoutAnimalMessage(kangarooName, kangarooTime)
   );
   assert.equal(
      messages.at(Position.SECOND),
      Strings.itinerary.confirmation.buildWarningWithoutAnimalMessage(lionName, lionTime)
   );
   assert.equal(
      messages.at(Position.THIRD),
      Strings.itinerary.confirmation.buildWarningLongWaitMessage(
         kangarooName,
         kangarooTime,
         Strings.entityPhrases.guardiansTalk
      )
   );
   assert.equal(
      messages.at(Position.FOURTH),
      Strings.itinerary.confirmation.buildWarningLongWaitMessage(
         lionName,
         lionTime,
         Strings.entityPhrases.guardiansTalk
      )
   );
});


test('Test_BuildItineraryBuildWarningSections_TestTimedWildEncounterOverlap_ExpectMessage', () => {
   const encounterName = 'Capybara';
   const encounterTime = '2:30 PM';

   const sections = ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections([
      {
         type: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         items: [{
            name: encounterName,
            start_time: encounterTime,
         }],
      },
   ]);

   assert.equal(sections.length, Position.SECOND);
   assert.equal(
      sections.at(Position.FIRST).message,
      Strings.itinerary.confirmation.buildWarningWildEncounterOverlapMessage(
         encounterName,
         encounterTime
      )
   );
});


test('Test_BuildItineraryBuildWarningSections_TestEmptyModules_ExpectSkipped', () => {
   const sections = ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections([
      { type: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS, items: [] },
      { type: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS, items: [] },
      { type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL, items: [] },
      { type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT, items: [] },
   ]);

   assert.deepEqual(sections, []);
});


test('Test_ShowItineraryBuildWarningsConfirmation_TestNoSections_ExpectCancelled', () => {
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
   const popup = document.querySelector('.tzg-popup');

   assert.equal(popup, null);
   assert.equal(cancelled, true);
});
