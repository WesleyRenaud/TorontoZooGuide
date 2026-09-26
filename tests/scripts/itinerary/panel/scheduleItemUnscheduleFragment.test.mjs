import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { ScheduleItemUnscheduleFragment } from '../../../../scripts/itinerary/panel/scheduleItemUnscheduleFragment.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
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
   const talkName = 'Amur Tiger';
   const issues = [
      { type: guardiansTalkConfig.issueType, items: [{ name: talkName }, { name: '' }] },
      { type: 'other', items: [{ name: 'Skip' }] },
   ];

   const names = ScheduleItemUnscheduleFragment.getNamesFromUnscheduleIssues(issues, guardiansTalkConfig);

   assert.deepEqual(names, [talkName]);
});


test('Test_GetPrimaryFromUnscheduleIssues_TestWithTime_ExpectItem', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const talkName = 'Amur Tiger';
   const talkTime = '11:00 AM';
   ItineraryItemFormatter.formatClockTime = () => talkTime;

   try {
      const item = ScheduleItemUnscheduleFragment.getPrimaryFromUnscheduleIssues([
         { type: guardiansTalkConfig.issueType, items: [{ name: talkName, start_time: talkTime }] },
      ], guardiansTalkConfig);

      assert.deepEqual(item, { [guardiansTalkConfig.nameKey]: talkName, [guardiansTalkConfig.timeKey]: talkTime });
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_GetPrimaryFromUnscheduleIssues_TestMissingName_ExpectNull', () => {
   const issues = [
      { type: wildEncounterConfig.issueType, items: [{ name: ' ' }] },
   ];

   const item = ScheduleItemUnscheduleFragment.getPrimaryFromUnscheduleIssues(issues, wildEncounterConfig);

   assert.equal(item, null);
});


test('Test_GetPrimaryFromUnscheduleIssues_TestMissingTime_ExpectNameOnly', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const encounterName = 'Giraffe Encounter';
   ItineraryItemFormatter.formatClockTime = () => '';

   try {
      const item = ScheduleItemUnscheduleFragment.getPrimaryFromUnscheduleIssues([
         { type: wildEncounterConfig.issueType, items: [{ name: encounterName }] },
      ], wildEncounterConfig);

      assert.deepEqual(item, { [wildEncounterConfig.nameKey]: encounterName });
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_ShowUnscheduleConfirmation_TestIssues_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   const encounterName = 'Giraffe Encounter';
   const encounterTime = '1:00 PM';
   const mountEl = { id: 'mount' };
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => encounterTime;

   try {
      ScheduleItemUnscheduleFragment.showUnscheduleConfirmation({
         issues: [{ type: wildEncounterConfig.issueType, items: [{ name: encounterName, start_time: encounterTime }] }],
         mountEl,
      }, wildEncounterConfig);

      const confirmation = calls.at(Position.FIRST);

      assert.equal(calls.length, 1);
      assert.equal(confirmation.title, wildEncounterConfig.getTitle());
      assert.equal(confirmation.message, wildEncounterConfig.getMessage(encounterName, encounterTime));
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});


test('Test_ShowUnscheduleConfirmation_TestEmptyIssues_ExpectNoPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   const mountEl = { id: 'mount' };
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => '1:00 PM';

   try {
      ScheduleItemUnscheduleFragment.showUnscheduleConfirmation({
         issues: [],
         mountEl,
      }, wildEncounterConfig);

      assert.equal(calls.length, 0);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});


test('Test_ShowUnscheduleConfirmation_TestWithoutTime_ExpectMessageWithoutTime', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   const talkName = 'Amur Tiger';
   const mountEl = { id: 'mount' };
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => '';

   try {
      ScheduleItemUnscheduleFragment.showUnscheduleConfirmation({
         issues: [{ type: guardiansTalkConfig.issueType, items: [{ name: talkName }] }],
         mountEl,
      }, guardiansTalkConfig);

      const confirmation = calls.at(Position.FIRST);

      assert.equal(calls.length, 1);
      assert.equal(confirmation.message, guardiansTalkConfig.getMessageWithoutTime(talkName));
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});
