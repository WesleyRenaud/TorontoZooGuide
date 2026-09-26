import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { WildEncounterUnscheduleFragment } from '../../../../scripts/itinerary/panel/wildEncounterUnscheduleFragment.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';

const issueType = ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS;


test('Test_GetWildEncounterNamesFromUnscheduleIssues_TestIssues_ExpectNames', () => {
   const encounterName = 'Giraffe Encounter';
   const issues = [
      { type: issueType, items: [{ name: encounterName }] },
   ];

   const names = WildEncounterUnscheduleFragment.getWildEncounterNamesFromUnscheduleIssues(issues);

   assert.deepEqual(names, [encounterName]);
});


test('Test_GetPrimaryWildEncounterFromUnscheduleIssues_TestWithTime_ExpectEncounter', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const encounterName = 'Giraffe Encounter';
   const encounterTime = '1:00 PM';
   ItineraryItemFormatter.formatClockTime = () => encounterTime;

   try {
      const encounter = WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues([
         { type: issueType, items: [{ name: encounterName, start_time: encounterTime }] },
      ]);

      assert.deepEqual(encounter, { encounterName, encounterTime });
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_ShowWildEncounterUnscheduleConfirmation_TestIssues_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalFormat = ItineraryItemFormatter.formatClockTime;
   const encounterName = 'Giraffe Encounter';
   const encounterTime = '1:00 PM';
   const mountEl = { id: 'mount' };
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryItemFormatter.formatClockTime = () => encounterTime;

   try {
      WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation({
         issues: [{ type: issueType, items: [{ name: encounterName, start_time: encounterTime }] }],
         mountEl,
      });

      const confirmation = calls.at(Position.FIRST);

      assert.equal(calls.length, 1);
      assert.equal(confirmation.title, Strings.itinerary.confirmation.wildEncounterRescheduleTitle);
      assert.equal(
         confirmation.message,
         Strings.itinerary.confirmation.wildEncounterRescheduleMessage(encounterName, encounterTime)
      );
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryItemFormatter.formatClockTime = originalFormat;
   }
});


test('Test_GetPrimaryWildEncounterFromUnscheduleIssues_TestMissingName_ExpectNull', () => {
   const issues = [
      { type: issueType, items: [{ name: ' ' }] },
   ];

   const encounter = WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues(issues);

   assert.equal(encounter, null);
});


test('Test_GetPrimaryWildEncounterFromUnscheduleIssues_TestMissingTime_ExpectNameOnly', () => {
   const original = ItineraryItemFormatter.formatClockTime;
   const encounterName = 'Giraffe Encounter';
   ItineraryItemFormatter.formatClockTime = () => '';

   try {
      const encounter = WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues([
         { type: issueType, items: [{ name: encounterName }] },
      ]);

      assert.deepEqual(encounter, { encounterName });
   } finally {
      ItineraryItemFormatter.formatClockTime = original;
   }
});


test('Test_ShowWildEncounterUnscheduleConfirmation_TestNoEncounter_ExpectNoPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const mountEl = { id: 'mount' };
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };

   try {
      WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation({
         issues: [],
         mountEl,
      });

      assert.equal(calls.length, 0);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
   }
});
