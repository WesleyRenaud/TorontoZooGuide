import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/scheduleItemWithoutAnimalFragment.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

const guardiansTalkConfig = Object.freeze({
   issueType: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
   nameKey: 'talkName',
   timeKey: 'talkTime',
   getTitle: () => Strings.itinerary.confirmation.guardiansTalkWithoutAnimalTitle,
   getMessage: (name, time) => Strings.itinerary.confirmation.guardiansTalkWithoutAnimalMessage(name, time),
   getMessageWithoutTime: (name) => Strings.itinerary.confirmation.guardiansTalkWithoutAnimalMessageWithoutTime(name),
   getBodyMessage: (name, time, strings) => strings.guardiansTalkWithoutAnimalMessage(name, time),
   getBodyMessageWithoutTime: (name, strings) => strings.guardiansTalkWithoutAnimalMessageWithoutTime(name),
   getConfirmPrompt: () => '',
});

const attractionConfig = Object.freeze({
   issueType: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
   nameKey: 'attractionName',
   timeKey: 'attractionTime',
   getTitle: () => Strings.itinerary.confirmation.attractionWithoutAnimalTitle,
   getMessage: (name, time) => {
      const strings = Strings.itinerary.confirmation;

      return `${strings.attractionWithoutAnimalBody(name, time)}${strings.attractionWithoutAnimalConfirmPrompt}`;
   },
   getMessageWithoutTime: (name) => {
      const strings = Strings.itinerary.confirmation;

      return `${strings.attractionWithoutAnimalBodyWithoutTime(name)}${strings.attractionWithoutAnimalConfirmPrompt}`;
   },
   getBodyMessage: (name, time, strings) => strings.attractionWithoutAnimalBody(name, time),
   getBodyMessageWithoutTime: (name, strings) => strings.attractionWithoutAnimalBodyWithoutTime(name),
   getConfirmPrompt: (strings) => strings.attractionWithoutAnimalConfirmPrompt,
});


test('Test_HasWithoutAnimalIssue_TestMatching_ExpectTrue', () => {
   const issues = [{ type: guardiansTalkConfig.issueType }];

   const hasIssue = ScheduleItemWithoutAnimalFragment.hasWithoutAnimalIssue(issues, guardiansTalkConfig);

   assert.equal(hasIssue, true);
});


test('Test_HasWithoutAnimalIssue_TestOtherType_ExpectFalse', () => {
   const issues = [{ type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT }];

   const hasIssue = ScheduleItemWithoutAnimalFragment.hasWithoutAnimalIssue(issues, guardiansTalkConfig);

   assert.equal(hasIssue, false);
});


test('Test_GetPrimaryFromWithoutAnimalIssues_TestItem_ExpectNoTime', () => {
   const talkName = 'Komodo Dragon';
   const issues = [{
      type: guardiansTalkConfig.issueType,
      items: [{ name: talkName }],
   }];

   const item = ScheduleItemWithoutAnimalFragment.getPrimaryFromWithoutAnimalIssues(
      issues,
      guardiansTalkConfig
   );

   assert.deepEqual(item, { [guardiansTalkConfig.nameKey]: talkName });
});


test('Test_GetItemsFromWithoutAnimalIssues_TestNamedItems_ExpectAll', () => {
   const kangaroo = 'Western Grey Kangaroo';
   const kangarooTime = '11:00 AM';
   const lion = 'African Lion';
   const lionTime = '2:00 PM';
   const issues = [{
      type: guardiansTalkConfig.issueType,
      items: [
         { name: kangaroo, start_time: kangarooTime },
         { name: lion, start_time: lionTime },
      ],
   }];

   const items = ScheduleItemWithoutAnimalFragment.getItemsFromWithoutAnimalIssues(
      issues,
      guardiansTalkConfig
   );

   assert.deepEqual(items, [
      { [guardiansTalkConfig.nameKey]: kangaroo, [guardiansTalkConfig.timeKey]: kangarooTime },
      { [guardiansTalkConfig.nameKey]: lion, [guardiansTalkConfig.timeKey]: lionTime },
   ]);
});


test('Test_GetNamesFromWithoutAnimalIssues_TestNamesAndBlanks_ExpectFiltered', () => {
   const kangaroo = 'Kangaroo Walk-Thru';
   const splashIsland = 'Splash Island';
   const issues = [{
      type: attractionConfig.issueType,
      items: [
         { name: `  ${kangaroo}  `, start_time: '11:00' },
         { name: '' },
         { name: splashIsland, start_time: '2:00 PM' },
      ],
   }];

   const names = ScheduleItemWithoutAnimalFragment.getNamesFromWithoutAnimalIssues(
      issues,
      attractionConfig
   );

   assert.deepEqual(names, [kangaroo, splashIsland]);
});


test('Test_WithoutAnimalMessage_TestWithTime_ExpectBody', () => {
   const attractionName = 'Splash Island';
   const attractionTime = '2:00 PM';

   const message = ScheduleItemWithoutAnimalFragment.withoutAnimalMessage({
      attractionName,
      attractionTime,
   }, attractionConfig);

   assert.equal(message, attractionConfig.getBodyMessage(attractionName, attractionTime, Strings.itinerary.confirmation));
});


test('Test_WithoutAnimalMessage_TestWithConfirmPrompt_ExpectPrompt', () => {
   const attractionName = 'Kangaroo Walk-Thru';

   const message = ScheduleItemWithoutAnimalFragment.withoutAnimalMessage({
      attractionName,
   }, attractionConfig, {
      includeConfirmPrompt: true,
      strings: Strings.itinerary.confirmation,
   });

   assert.equal(message, attractionConfig.getMessageWithoutTime(attractionName));
});


test('Test_ShowWithoutAnimalConfirmation_TestMessage_ExpectNoTime', () => {
   const talkName = 'Komodo Dragon';
   let confirmed = false;

   ScheduleItemWithoutAnimalFragment.showWithoutAnimalConfirmation({
      issues: [{
         type: guardiansTalkConfig.issueType,
         items: [{ name: talkName }],
      }],
      onConfirm: () => {
         confirmed = true;
      },
   }, guardiansTalkConfig);

   const popupMessage = document.querySelector('.tzg-popup-message');
   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(popupMessage?.textContent, guardiansTalkConfig.getMessageWithoutTime(talkName));
   assert.equal(confirmed, true);
});


test('Test_ShowWithoutAnimalConfirmation_TestMultiple_ExpectNoOp', () => {
   ScheduleItemWithoutAnimalFragment.showWithoutAnimalConfirmation({
      issues: [{
         type: guardiansTalkConfig.issueType,
         items: [
            { name: 'Western Grey Kangaroo' },
            { name: 'African Lion' },
         ],
      }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   }, guardiansTalkConfig);

   const popup = document.querySelector('.tzg-popup');

   assert.equal(popup, null);
});


test('Test_ShowWithoutAnimalConfirmation_TestMissingName_ExpectNoOp', () => {
   ScheduleItemWithoutAnimalFragment.showWithoutAnimalConfirmation({
      issues: [{ type: attractionConfig.issueType, items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   }, attractionConfig);

   const popup = document.querySelector('.tzg-popup');

   assert.equal(popup, null);
});
