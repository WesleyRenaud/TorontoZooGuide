import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { GuardiansTalkUnscheduleFragment } from '../../../../scripts/itinerary/panel/guardiansTalkUnscheduleFragment.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';

const issueType = ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;


test('Test_GetGuardiansTalkNamesFromUnscheduleIssues_TestIssues_ExpectNames', () => {
   const talkName = 'Amur Tiger';
   const issues = [
      { type: issueType, items: [{ name: talkName }, { name: '' }] },
      { type: 'other', items: [{ name: 'Skip' }] },
   ];

   const names = GuardiansTalkUnscheduleFragment.getGuardiansTalkNamesFromUnscheduleIssues(issues);

   assert.deepEqual(names, [talkName]);
});


test('Test_GetPrimaryGuardiansTalkFromUnscheduleIssues_TestWithTime_ExpectTalk', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const talkName = 'Amur Tiger';
   const talkTime = '11:00 AM';
   ItineraryItemFormatter.formatClockTime = () => talkTime;

   try {
      const talk = GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues([
         { type: issueType, items: [{ name: talkName, start_time: talkTime }] },
      ]);

      assert.deepEqual(talk, { talkName, talkTime });
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_ShowGuardiansTalkUnscheduleConfirmation_TestIssues_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   const talkName = 'Amur Tiger';
   const mountEl = { id: 'mount' };
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => '';

   try {
      GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation({
         issues: [{ type: issueType, items: [{ name: talkName }] }],
         mountEl,
      });

      const confirmation = calls.at(Position.FIRST);

      assert.equal(calls.length, 1);
      assert.equal(confirmation.title, Strings.itinerary.confirmation.guardiansTalkRescheduleTitle);
      assert.equal(
         confirmation.message,
         Strings.itinerary.confirmation.guardiansTalkRescheduleMessageWithoutTime(talkName)
      );
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});


test('Test_ShowGuardiansTalkUnscheduleConfirmation_TestEmptyIssues_ExpectNoPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   const mountEl = { id: 'mount' };
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => '';

   try {
      GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation({
         issues: [],
         mountEl,
      });

      assert.equal(calls.length, 0);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});
