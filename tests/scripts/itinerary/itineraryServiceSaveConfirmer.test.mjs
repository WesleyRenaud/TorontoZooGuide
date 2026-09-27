import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
import { ItineraryConfirmationResult } from '../../../scripts/itinerary/itineraryConfirmationResult.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryServiceSaveConfirmer } from '../../../scripts/itinerary/itineraryServiceSaveConfirmer.js';
import { ItineraryShape } from '../../../scripts/itinerary/itineraryShape.js';
import { AttractionWithoutAnimalFragment } from '../../../scripts/itinerary/panel/attractionWithoutAnimalFragment.js';
import { EarlyAdmissionFragment } from '../../../scripts/itinerary/panel/earlyAdmissionFragment.js';
import { FixedTimeItemLongWaitFragment } from '../../../scripts/itinerary/panel/fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from '../../../scripts/itinerary/panel/guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from '../../../scripts/itinerary/panel/guardiansTalkWithoutAnimalFragment.js';
import { ItineraryBuildWarningsFragment } from '../../../scripts/itinerary/panel/itineraryBuildWarningsFragment.js';
import { ScheduleTimeConflictFragment } from '../../../scripts/itinerary/panel/scheduleTimeConflictFragment.js';
import { ShortVisitFragment } from '../../../scripts/itinerary/panel/shortVisitFragment.js';
import { VisitWindowOverflowFragment } from '../../../scripts/itinerary/panel/visitWindowOverflowFragment.js';
import { WildEncounterUnscheduleFragment } from '../../../scripts/itinerary/panel/wildEncounterUnscheduleFragment.js';
import { WildEncounterConflictResolver } from '../../../scripts/itinerary/wizard/wildEncounterConflictResolver.js';
import { Position } from '../../../scripts/shared/enums/position.js';

function _stubErrorTypeChecks(activeType) {
   const originals = {
      success: ItineraryErrorTypes.isItinerarySuccess,
      conflict: ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation,
      unschedule: ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation,
      talkWithout: ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation,
      attractionWithout: ItineraryErrorTypes.requiresAttractionWithoutAnimalConfirmation,
      longWait: ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation,
      wildUnschedule: ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation,
      shortVisit: ItineraryErrorTypes.requiresShortVisitConfirmation,
      earlyAdmission: ItineraryErrorTypes.requiresEarlyAdmissionConfirmation,
      overflow: ItineraryErrorTypes.requiresVisitWindowOverflowConfirmation,
      multiWarnings: ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings,
   };

   ItineraryErrorTypes.isItinerarySuccess = (type) => type === 'success';
   ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation = (type) => (
      type === 'conflict' && activeType === 'conflict'
   );
   ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation = (type) => (
      type === 'talkUnschedule' && activeType === 'talkUnschedule'
   );
   ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation = (type) => (
      type === 'talkWithout' && activeType === 'talkWithout'
   );
   ItineraryErrorTypes.requiresAttractionWithoutAnimalConfirmation = (type) => (
      type === 'attractionWithout' && activeType === 'attractionWithout'
   );
   ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation = (type) => (
      type === 'longWait' && activeType === 'longWait'
   );
   ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation = (type) => (
      type === 'wildUnschedule' && activeType === 'wildUnschedule'
   );
   ItineraryErrorTypes.requiresShortVisitConfirmation = (type) => (
      type === 'shortVisit' && activeType === 'shortVisit'
   );
   ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = (type) => (
      type === 'earlyAdmission' && activeType === 'earlyAdmission'
   );
   ItineraryErrorTypes.requiresVisitWindowOverflowConfirmation = (type) => (
      type === 'overflow' && activeType === 'overflow'
   );
   ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings = (issues) => (
      activeType === 'multiWarnings' && Boolean(issues?.length)
   );

   return () => {
      ItineraryErrorTypes.isItinerarySuccess = originals.success;
      ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation = originals.conflict;
      ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation = originals.unschedule;
      ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation = originals.talkWithout;
      ItineraryErrorTypes.requiresAttractionWithoutAnimalConfirmation = originals.attractionWithout;
      ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation = originals.longWait;
      ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation = originals.wildUnschedule;
      ItineraryErrorTypes.requiresShortVisitConfirmation = originals.shortVisit;
      ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = originals.earlyAdmission;
      ItineraryErrorTypes.requiresVisitWindowOverflowConfirmation = originals.overflow;
      ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings = originals.multiWarnings;
   };
}

async function _assertConfirmationFlagPath({
   activeType,
   errorType,
   fragment,
   showMethod,
   expectedFlag,
}) {
   const originalRequest = ItineraryClient.setItineraryRequest;
   const originalShow = fragment[showMethod];
   const restore = _stubErrorTypeChecks(activeType);
   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation;
   const payloads = [];
   const date = '2026-06-15';

   ItineraryClient.setItineraryRequest = async () => ({
      errorType,
      issues: [{ type: errorType }],
   });
   fragment[showMethod] = () => {};
   ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation = async (options) => {
      payloads.push(options.buildConfirmedPayload());
      return { result: { errorType: 'success' }, diffBaseline: options.diffBaseline };
   };

   try {
      await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations({ date });

      assert.equal(payloads[Position.FIRST][expectedFlag], true);
   } finally {
      ItineraryClient.setItineraryRequest = originalRequest;
      fragment[showMethod] = originalShow;
      ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation = originalConfirm;
      restore();
   }
}


test('Test_CreateConfirmedSetItineraryResult_TestArgs_ExpectWrapped', () => {
   const result = { ok: true };
   const date = '2026-06-15';
   const diffBaseline = { date };

   const confirmed = ItineraryServiceSaveConfirmer.createConfirmedSetItineraryResult(
      result,
      diffBaseline
   );

   assert.equal(confirmed.result, result);
   assert.equal(confirmed.diffBaseline, diffBaseline);
});


test('Test_GetSetItineraryResultPayload_TestWithItinerary_ExpectPayload', () => {
   const original = ItineraryShape.toSetItineraryPayload;
   const date = '2026-06-15';
   ItineraryShape.toSetItineraryPayload = (itinerary) => ({ date: itinerary.date });

   try {
      const payload = ItineraryServiceSaveConfirmer.getSetItineraryResultPayload({
         itinerary: { date },
      });

      assert.equal(payload.date, date);
   } finally {
      ItineraryShape.toSetItineraryPayload = original;
   }
});


test('Test_GetSetItineraryResultPayload_TestEmpty_ExpectEmptyObject', () => {
   const original = ItineraryShape.toSetItineraryPayload;
   ItineraryShape.toSetItineraryPayload = (itinerary) => ({ date: itinerary.date });

   try {
      const payload = ItineraryServiceSaveConfirmer.getSetItineraryResultPayload({});

      assert.deepEqual(payload, {});
   } finally {
      ItineraryShape.toSetItineraryPayload = original;
   }
});


test('Test_RequestSetItineraryConfirmation_TestConfirm_ExpectConfirmedResult', async () => {
   const originalRequest = ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations;
   const originalCancelled = ItineraryConfirmationResult.createItineraryConfirmationCancelledResult;
   const date = '2026-06-15';
   const confirmedPayload = { date, confirmed: true };
   const diffBaseline = { base: true };
   const beforeConfirmCalls = [];
   let confirmHandler = null;
   ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = async (payload, baseline) => ({
      result: { confirmed: true, payload },
      diffBaseline: baseline,
   });
   ItineraryConfirmationResult.createItineraryConfirmationCancelledResult = ({ issues }) => ({
      cancelled: true,
      issues,
   });

   try {
      const confirmedPromise = ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
         showConfirmation: ({ onConfirm }) => {
            confirmHandler = onConfirm;
         },
         initialResult: { issues: ['a'] },
         payload: { date },
         diffBaseline,
         buildConfirmedPayload: () => confirmedPayload,
         beforeConfirm: async (...args) => {
            beforeConfirmCalls.push(args);
         },
      });
      const doNotShowAgain = true;
      await confirmHandler({ doNotShowAgain });
      const confirmed = await confirmedPromise;

      assert.equal(beforeConfirmCalls.length, 1);
      assert.deepEqual(beforeConfirmCalls[Position.FIRST], [{ doNotShowAgain }]);
      assert.equal(confirmed.result.confirmed, true);
      assert.deepEqual(confirmed.result.payload, confirmedPayload);
      assert.equal(confirmed.diffBaseline, diffBaseline);
   } finally {
      ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = originalRequest;
      ItineraryConfirmationResult.createItineraryConfirmationCancelledResult = originalCancelled;
   }
});


test('Test_RequestSetItineraryConfirmation_TestCancel_ExpectCancelledResult', async () => {
   const originalRequest = ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations;
   const originalCancelled = ItineraryConfirmationResult.createItineraryConfirmationCancelledResult;
   const issues = ['b'];
   const cancelledResult = { cancelled: true, issues };
   let cancelHandler = null;
   ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = async (payload, baseline) => ({
      result: { confirmed: true, payload },
      diffBaseline: baseline,
   });
   ItineraryConfirmationResult.createItineraryConfirmationCancelledResult = ({ issues: nextIssues }) => ({
      cancelled: true,
      issues: nextIssues,
   });

   try {
      const cancelledPromise = ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
         showConfirmation: ({ onCancel }) => {
            cancelHandler = onCancel;
         },
         initialResult: { issues },
         payload: {},
         diffBaseline: null,
         buildConfirmedPayload: () => ({}),
      });
      cancelHandler();
      const cancelled = await cancelledPromise;

      assert.deepEqual(cancelled, cancelledResult);
   } finally {
      ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = originalRequest;
      ItineraryConfirmationResult.createItineraryConfirmationCancelledResult = originalCancelled;
   }
});


test('Test_RequestSetItineraryWithConfirmations_TestSuccess_ExpectConfirmed', async () => {
   const originalRequest = ItineraryClient.setItineraryRequest;
   const restore = _stubErrorTypeChecks(null);
   const date = '2026-06-15';
   const diffBaseline = 'base';
   const apiResult = { errorType: 'success', itinerary: {} };
   ItineraryClient.setItineraryRequest = async () => apiResult;

   try {
      const confirmed = await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations(
         { date },
         diffBaseline
      );

      assert.equal(confirmed.result, apiResult);
      assert.equal(confirmed.diffBaseline, diffBaseline);
   } finally {
      ItineraryClient.setItineraryRequest = originalRequest;
      restore();
   }
});


test('Test_RequestSetItineraryWithConfirmations_TestConflictPath_ExpectConfirmation', async () => {
   const originalRequest = ItineraryClient.setItineraryRequest;
   const originalShow = ScheduleTimeConflictFragment.showScheduleTimeConflictConfirmation;
   const originalApply = WildEncounterConflictResolver.applyConflictSelectionToItineraryDraft;
   const originalPayload = ItineraryServiceSaveConfirmer.getSetItineraryResultPayload;
   const restore = _stubErrorTypeChecks('conflict');
   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation;
   const date = '2026-06-15';
   const species = 'Lion';
   let shown = null;
   let confirmCalls = 0;
   ItineraryClient.setItineraryRequest = async (payload) => {
      if (payload.overridingConflictingGuardiansTalks) {
         return { errorType: 'success', itinerary: { date } };
      }
      return {
         errorType: 'conflict',
         issues: [{ type: 'conflict' }],
         itinerary: { animals: [{ species }], attractions: [] },
      };
   };
   ScheduleTimeConflictFragment.showScheduleTimeConflictConfirmation = (args) => {
      shown = args;
      void args.onConfirm([{ selected: true }]);
   };
   WildEncounterConflictResolver.applyConflictSelectionToItineraryDraft = () => ({
      guardiansTalks: [{ name: 'Talk' }],
      wildEncounters: [{ name: 'Encounter' }],
   });
   ItineraryServiceSaveConfirmer.getSetItineraryResultPayload = () => ({
      animals: [{ species }],
      attractions: [],
   });
   ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation = async (options) => {
      confirmCalls += 1;
      options.showConfirmation({
         issues: options.initialResult.issues,
         onConfirm: async (...args) => {
            const payload = options.buildConfirmedPayload(...args);
            assert.equal(payload.overridingConflictingGuardiansTalks, true);
            return options.getConfirmedDiffBaseline(payload);
         },
         onCancel: () => {},
      });
      return { result: { errorType: 'success' }, diffBaseline: null };
   };

   try {
      const result = await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations({
         guardiansTalks: [],
         wildEncounters: [],
      });

      assert.equal(confirmCalls, 1);
      assert.equal(result.result.errorType, 'success');
      assert.ok(shown);
   } finally {
      ItineraryClient.setItineraryRequest = originalRequest;
      ScheduleTimeConflictFragment.showScheduleTimeConflictConfirmation = originalShow;
      WildEncounterConflictResolver.applyConflictSelectionToItineraryDraft = originalApply;
      ItineraryServiceSaveConfirmer.getSetItineraryResultPayload = originalPayload;
      ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation = originalConfirm;
      restore();
   }
});


test('Test_RequestSetItineraryWithConfirmations_TestTalkUnschedule_ExpectFlag', async () => {
   await _assertConfirmationFlagPath({
      activeType: 'talkUnschedule',
      errorType: 'talkUnschedule',
      fragment: GuardiansTalkUnscheduleFragment,
      showMethod: 'showGuardiansTalkUnscheduleConfirmation',
      expectedFlag: 'confirmingGuardiansTalkUnschedule',
   });
});


test('Test_RequestSetItineraryWithConfirmations_TestTalkWithoutAnimal_ExpectFlag', async () => {
   await _assertConfirmationFlagPath({
      activeType: 'talkWithout',
      errorType: 'talkWithout',
      fragment: GuardiansTalkWithoutAnimalFragment,
      showMethod: 'showGuardiansTalkWithoutAnimalConfirmation',
      expectedFlag: 'confirmingGuardiansTalkWithoutAnimal',
   });
});


test('Test_RequestSetItineraryWithConfirmations_TestAttractionWithoutAnimal_ExpectFlag', async () => {
   await _assertConfirmationFlagPath({
      activeType: 'attractionWithout',
      errorType: 'attractionWithout',
      fragment: AttractionWithoutAnimalFragment,
      showMethod: 'showAttractionWithoutAnimalConfirmation',
      expectedFlag: 'confirmingAttractionWithoutAnimal',
   });
});


test('Test_RequestSetItineraryWithConfirmations_TestLongWait_ExpectFlag', async () => {
   await _assertConfirmationFlagPath({
      activeType: 'longWait',
      errorType: 'longWait',
      fragment: FixedTimeItemLongWaitFragment,
      showMethod: 'showFixedTimeItemLongWaitConfirmation',
      expectedFlag: 'confirmingFixedTimeItemLongWait',
   });
});


test('Test_RequestSetItineraryWithConfirmations_TestWildUnschedule_ExpectFlag', async () => {
   await _assertConfirmationFlagPath({
      activeType: 'wildUnschedule',
      errorType: 'wildUnschedule',
      fragment: WildEncounterUnscheduleFragment,
      showMethod: 'showWildEncounterUnscheduleConfirmation',
      expectedFlag: 'confirmingWildEncounterUnschedule',
   });
});


test('Test_RequestSetItineraryWithConfirmations_TestEarlyAdmission_ExpectFlag', async () => {
   await _assertConfirmationFlagPath({
      activeType: 'earlyAdmission',
      errorType: 'earlyAdmission',
      fragment: EarlyAdmissionFragment,
      showMethod: 'showEarlyAdmissionConfirmation',
      expectedFlag: 'confirmingEarlyAdmission',
   });
});


test('Test_RequestSetItineraryWithConfirmations_TestOverflow_ExpectFlag', async () => {
   await _assertConfirmationFlagPath({
      activeType: 'overflow',
      errorType: 'overflow',
      fragment: VisitWindowOverflowFragment,
      showMethod: 'showVisitWindowOverflowConfirmation',
      expectedFlag: 'confirmingVisitWindowOverflow',
   });
});


test('Test_RequestSetItineraryWithConfirmations_TestShortVisit_ExpectFlag', async () => {
   await _assertConfirmationFlagPath({
      activeType: 'shortVisit',
      errorType: 'shortVisit',
      fragment: ShortVisitFragment,
      showMethod: 'showShortVisitConfirmation',
      expectedFlag: 'confirmingShortVisit',
   });
});


test('Test_RequestSetItineraryWithConfirmations_TestMultiWarnings_ExpectMergedOptions', async () => {
   const originalRequest = ItineraryClient.setItineraryRequest;
   const originalShow = ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation;
   const originalBuild = ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings;
   const restore = _stubErrorTypeChecks('multiWarnings');
   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation;
   const date = '2026-06-15';
   const confirmingGuardiansTalkUnschedule = true;
   const confirmingFixedTimeItemLongWait = true;
   let payload = null;
   ItineraryClient.setItineraryRequest = async () => ({
      errorType: 'other',
      issues: [{ type: 'a' }, { type: 'b' }],
   });
   ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation = () => {};
   ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings = () => ({
      confirmingGuardiansTalkUnschedule,
      confirmingFixedTimeItemLongWait,
   });
   ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation = async (options) => {
      payload = options.buildConfirmedPayload();
      return { result: { errorType: 'success' }, diffBaseline: null };
   };

   try {
      await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations({ date });

      assert.equal(payload.confirmingGuardiansTalkUnschedule, confirmingGuardiansTalkUnschedule);
      assert.equal(payload.confirmingFixedTimeItemLongWait, confirmingFixedTimeItemLongWait);
   } finally {
      ItineraryClient.setItineraryRequest = originalRequest;
      ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation = originalShow;
      ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings = originalBuild;
      ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation = originalConfirm;
      restore();
   }
});


test('Test_RequestSetItineraryWithConfirmations_TestUnhandledError_ExpectPassthrough', async () => {
   const originalRequest = ItineraryClient.setItineraryRequest;
   const restore = _stubErrorTypeChecks(null);
   const date = '2026-06-15';
   const diffBaseline = 'base';
   const apiResult = { errorType: 'unknown', issues: [] };
   ItineraryClient.setItineraryRequest = async () => apiResult;

   try {
      const confirmed = await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations(
         { date },
         diffBaseline
      );

      assert.equal(confirmed.result, apiResult);
      assert.equal(confirmed.diffBaseline, diffBaseline);
   } finally {
      ItineraryClient.setItineraryRequest = originalRequest;
      restore();
   }
});
