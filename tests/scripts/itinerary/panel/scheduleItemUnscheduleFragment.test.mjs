import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemUnscheduleFragment } from '../../../../scripts/itinerary/panel/scheduleItemUnscheduleFragment.js';
import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Strings } from '../../../../scripts/strings.js';

const guardiansTalkConfig = Object.freeze({
   issueType: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
   nameKey: 'talkName',
   timeKey: 'talkTime',
   getTitle: () => Strings.itinerary.confirmation.guardiansTalkRescheduleTitle,
   getMessage: (name, time) => Strings.itinerary.confirmation.guardiansTalkRescheduleMessage(name, time),
   getMessageWithoutTime: (name) => Strings.itinerary.confirmation.guardiansTalkRescheduleMessageWithoutTime(name),
});

const wildEncounterConfig = Object.freeze({
   issueType: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
   nameKey: 'encounterName',
   timeKey: 'encounterTime',
   getTitle: () => Strings.itinerary.confirmation.wildEncounterRescheduleTitle,
   getMessage: (name, time) => Strings.itinerary.confirmation.wildEncounterRescheduleMessage(name, time),
   getMessageWithoutTime: (name) => Strings.itinerary.confirmation.wildEncounterRescheduleMessageWithoutTime(name),
});

test('Test_GetNamesFromUnscheduleIssues_TestIssues_ExpectNames', () => {
   assert.deepEqual(
      ScheduleItemUnscheduleFragment.getNamesFromUnscheduleIssues([
         { type: guardiansTalkConfig.issueType, items: [{ name: 'Amur Tiger' }, { name: '' }] },
         { type: 'other', items: [{ name: 'Skip' }] },
      ], guardiansTalkConfig),
      ['Amur Tiger']
   );
});

test('Test_GetPrimaryFromUnscheduleIssues_TestWithTime_ExpectItem', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   ItineraryItemFormatter.formatClockTime = () => '11:00 AM';

   try {
      assert.deepEqual(
         ScheduleItemUnscheduleFragment.getPrimaryFromUnscheduleIssues([
            { type: guardiansTalkConfig.issueType, items: [{ name: 'Amur Tiger', start_time: '11:00 AM' }] },
         ], guardiansTalkConfig),
         { talkName: 'Amur Tiger', talkTime: '11:00 AM' }
      );
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});

test('Test_GetPrimaryFromUnscheduleIssues_TestMissingName_ExpectNull', () => {
   assert.equal(
      ScheduleItemUnscheduleFragment.getPrimaryFromUnscheduleIssues([
         { type: wildEncounterConfig.issueType, items: [{ name: ' ' }] },
      ], wildEncounterConfig),
      null
   );
});

test('Test_GetPrimaryFromUnscheduleIssues_TestMissingTime_ExpectNameOnly', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   ItineraryItemFormatter.formatClockTime = () => '';

   try {
      assert.deepEqual(
         ScheduleItemUnscheduleFragment.getPrimaryFromUnscheduleIssues([
            { type: wildEncounterConfig.issueType, items: [{ name: 'Giraffe Encounter' }] },
         ], wildEncounterConfig),
         { encounterName: 'Giraffe Encounter' }
      );
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});

test('Test_ShowUnscheduleConfirmation_TestIssues_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => '1:00 PM';

   try {
      ScheduleItemUnscheduleFragment.showUnscheduleConfirmation({
         issues: [{ type: wildEncounterConfig.issueType, items: [{ name: 'Giraffe Encounter', start_time: '1:00 PM' }] }],
         mountEl: { id: 'mount' },
      }, wildEncounterConfig);
      assert.equal(calls.length, 1);
      assert.equal(calls[0].title, Strings.itinerary.confirmation.wildEncounterRescheduleTitle);
      assert.equal(
         calls[0].message,
         Strings.itinerary.confirmation.wildEncounterRescheduleMessage('Giraffe Encounter', '1:00 PM')
      );

      ScheduleItemUnscheduleFragment.showUnscheduleConfirmation({
         issues: [],
         mountEl: { id: 'mount' },
      }, wildEncounterConfig);
      assert.equal(calls.length, 1);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});

test('Test_ShowUnscheduleConfirmation_TestWithoutTime_ExpectMessageWithoutTime', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => '';

   try {
      ScheduleItemUnscheduleFragment.showUnscheduleConfirmation({
         issues: [{ type: guardiansTalkConfig.issueType, items: [{ name: 'Amur Tiger' }] }],
         mountEl: { id: 'mount' },
      }, guardiansTalkConfig);
      assert.equal(calls.length, 1);
      assert.equal(
         calls[0].message,
         Strings.itinerary.confirmation.guardiansTalkRescheduleMessageWithoutTime('Amur Tiger')
      );
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});
