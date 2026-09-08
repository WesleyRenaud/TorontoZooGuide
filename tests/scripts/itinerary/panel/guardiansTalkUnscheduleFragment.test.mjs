import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkUnscheduleFragment } from '../../../../scripts/itinerary/panel/guardiansTalkUnscheduleFragment.js';
import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { Strings } from '../../../../scripts/strings.js';

const issueType = GuardiansTalkUnscheduleFragment.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS_ISSUE;

test('Test_GetGuardiansTalkNamesFromUnscheduleIssues_TestIssues_ExpectNames', () => {
   assert.deepEqual(
      GuardiansTalkUnscheduleFragment.getGuardiansTalkNamesFromUnscheduleIssues([
         { type: issueType, items: [{ name: 'Amur Tiger' }, { name: '' }] },
         { type: 'other', items: [{ name: 'Skip' }] },
      ]),
      ['Amur Tiger']
   );
});

test('Test_GetPrimaryGuardiansTalkFromUnscheduleIssues_TestWithTime_ExpectTalk', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   ItineraryItemFormatter.formatClockTime = () => '11:00 AM';

   try {
      assert.deepEqual(
         GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues([
            { type: issueType, items: [{ name: 'Amur Tiger', start_time: '11:00 AM' }] },
         ]),
         { talkName: 'Amur Tiger', talkTime: '11:00 AM' }
      );
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});

test('Test_ShowGuardiansTalkUnscheduleConfirmation_TestIssues_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => '';

   try {
      GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation({
         issues: [{ type: issueType, items: [{ name: 'Amur Tiger' }] }],
         mountEl: { id: 'mount' },
      });
      assert.equal(calls.length, 1);
      assert.equal(calls[0].title, Strings.itinerary.confirmation.guardiansTalkRescheduleTitle);
      assert.equal(
         calls[0].message,
         Strings.itinerary.confirmation.guardiansTalkRescheduleMessageWithoutTime('Amur Tiger')
      );

      GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation({
         issues: [],
         mountEl: { id: 'mount' },
      });
      assert.equal(calls.length, 1);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});
