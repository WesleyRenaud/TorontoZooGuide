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

test('Test_HasWithoutAnimalIssue_TestMatching_ExpectDetected', () => {
   assert.equal(
      ScheduleItemWithoutAnimalFragment.hasWithoutAnimalIssue([
         { type: guardiansTalkConfig.issueType },
      ], guardiansTalkConfig),
      true
   );
   assert.equal(
      ScheduleItemWithoutAnimalFragment.hasWithoutAnimalIssue([
         { type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT },
      ], guardiansTalkConfig),
      false
   );
});

test('Test_GetPrimaryFromWithoutAnimalIssues_TestItem_ExpectNoTime', () => {
   assert.deepEqual(
      ScheduleItemWithoutAnimalFragment.getPrimaryFromWithoutAnimalIssues([
         {
            type: guardiansTalkConfig.issueType,
            items: [{ name: 'Komodo Dragon' }],
         },
      ], guardiansTalkConfig),
      { talkName: 'Komodo Dragon' }
   );
});

test('Test_GetItemsFromWithoutAnimalIssues_TestNamedItems_ExpectAll', () => {
   assert.deepEqual(
      ScheduleItemWithoutAnimalFragment.getItemsFromWithoutAnimalIssues([{
         type: guardiansTalkConfig.issueType,
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
      }], guardiansTalkConfig),
      [
         {
            talkName: 'Western Grey Kangaroo',
            talkTime: '11:00 AM',
         },
         {
            talkName: 'African Lion',
            talkTime: '2:00 PM',
         },
      ]
   );
});

test('Test_GetNamesFromWithoutAnimalIssues_TestNamesAndBlanks_ExpectFiltered', () => {
   assert.deepEqual(
      ScheduleItemWithoutAnimalFragment.getNamesFromWithoutAnimalIssues([{
         type: attractionConfig.issueType,
         items: [
            { name: '  Kangaroo Walk-Thru  ', start_time: '11:00' },
            { name: '' },
            { name: 'Splash Island', start_time: '2:00 PM' },
         ],
      }], attractionConfig),
      ['Kangaroo Walk-Thru', 'Splash Island']
   );
});

test('Test_WithoutAnimalMessage_TestWithTime_ExpectBody', () => {
   assert.match(
      ScheduleItemWithoutAnimalFragment.withoutAnimalMessage({
         attractionName: 'Splash Island',
         attractionTime: '2:00 PM',
      }, attractionConfig),
      /Splash Island.*2:00 PM/
   );
});

test('Test_WithoutAnimalMessage_TestWithConfirmPrompt_ExpectPrompt', () => {
   const message = ScheduleItemWithoutAnimalFragment.withoutAnimalMessage({
      attractionName: 'Kangaroo Walk-Thru',
   }, attractionConfig, {
      includeConfirmPrompt: true,
      strings: Strings.itinerary.confirmation,
   });

   assert.match(message, /Kangaroo Walk-Thru/);
   assert.match(message, /Do you still want to keep it on your plan/);
});

test('Test_ShowWithoutAnimalConfirmation_TestMessage_ExpectNoTime', () => {
   let confirmed = false;

   ScheduleItemWithoutAnimalFragment.showWithoutAnimalConfirmation({
      issues: [{
         type: guardiansTalkConfig.issueType,
         items: [{ name: 'Komodo Dragon' }],
      }],
      onConfirm: () => {
         confirmed = true;
      },
   }, guardiansTalkConfig);

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage?.textContent,
      'The Komodo Dragon guardians talk does not match an animal on your itinerary. Do you still want to keep it on your plan?'
   );

   document.querySelector('.tzg-popup-confirm')?.click();

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

   assert.equal(document.querySelector('.tzg-popup'), null);
});

test('Test_ShowWithoutAnimalConfirmation_TestMissingName_ExpectNoOp', () => {
   ScheduleItemWithoutAnimalFragment.showWithoutAnimalConfirmation({
      issues: [{ type: attractionConfig.issueType, items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   }, attractionConfig);

   assert.equal(document.querySelector('.tzg-popup'), null);
});
