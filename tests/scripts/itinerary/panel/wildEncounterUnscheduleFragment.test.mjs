import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterUnscheduleFragment } from '../../../../scripts/itinerary/panel/wildEncounterUnscheduleFragment.js';
import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { Strings } from '../../../../scripts/strings.js';

const issueType = WildEncounterUnscheduleFragment.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS_ISSUE;

test('Test_GetWildEncounterNamesFromUnscheduleIssues_TestIssues_ExpectNames', () => {
   assert.deepEqual(
      WildEncounterUnscheduleFragment.getWildEncounterNamesFromUnscheduleIssues([
         { type: issueType, items: [{ name: 'Giraffe Encounter' }] },
      ]),
      ['Giraffe Encounter']
   );
});

test('Test_GetPrimaryWildEncounterFromUnscheduleIssues_TestWithTime_ExpectEncounter', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   ItineraryItemFormatter.formatClockTime = () => '1:00 PM';

   try {
      assert.deepEqual(
         WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues([
            { type: issueType, items: [{ name: 'Giraffe Encounter', start_time: '1:00 PM' }] },
         ]),
         { encounterName: 'Giraffe Encounter', encounterTime: '1:00 PM' }
      );
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});

test('Test_ShowWildEncounterUnscheduleConfirmation_TestIssues_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => '1:00 PM';

   try {
      WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation({
         issues: [{ type: issueType, items: [{ name: 'Giraffe Encounter', start_time: '1:00 PM' }] }],
         mountEl: { id: 'mount' },
      });
      assert.equal(calls.length, 1);
      assert.equal(calls[0].title, Strings.itinerary.confirmation.wildEncounterRescheduleTitle);
      assert.equal(
         calls[0].message,
         Strings.itinerary.confirmation.wildEncounterRescheduleMessage('Giraffe Encounter', '1:00 PM')
      );
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});
