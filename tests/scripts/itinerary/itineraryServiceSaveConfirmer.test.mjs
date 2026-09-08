import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
import { ItineraryConfirmationResult } from '../../../scripts/itinerary/itineraryConfirmationResult.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryServiceSaveConfirmer } from '../../../scripts/itinerary/itineraryServiceSaveConfirmer.js';
import { ItineraryShape } from '../../../scripts/itinerary/itineraryShape.js';
import { AttractionWithoutAnimalFragment } from '../../../scripts/itinerary/panel/attractionWithoutAnimalFragment.js';
import { FixedTimeItemLongWaitFragment } from '../../../scripts/itinerary/panel/fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from '../../../scripts/itinerary/panel/guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from '../../../scripts/itinerary/panel/guardiansTalkWithoutAnimalFragment.js';
import { ItineraryBuildWarningsFragment } from '../../../scripts/itinerary/panel/itineraryBuildWarningsFragment.js';
import { ScheduleTimeConflictFragment } from '../../../scripts/itinerary/panel/scheduleTimeConflictFragment.js';
import { WildEncounterUnscheduleFragment } from '../../../scripts/itinerary/panel/wildEncounterUnscheduleFragment.js';
import { WildEncounterConflictResolver } from '../../../scripts/itinerary/wizard/wildEncounterConflictResolver.js';

function _stubErrorTypeChecks(activeType) {
   const originals = {
      success: ItineraryErrorTypes.isItinerarySuccess,
      conflict: ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation,
      unschedule: ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation,
      talkWithout: ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation,
      attractionWithout: ItineraryErrorTypes.requiresAttractionWithoutAnimalConfirmation,
      longWait: ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation,
      wildUnschedule: ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation,
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
      await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations({ date: '2026-06-15' });
      assert.equal(payloads[0][expectedFlag], true);
   } finally {
      ItineraryClient.setItineraryRequest = originalRequest;
      fragment[showMethod] = originalShow;
      ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation = originalConfirm;
      restore();
   }
}

test('Test_CreateConfirmedSetItineraryResult_TestArgs_ExpectWrapped', () => {
   assert.deepEqual(
      ItineraryServiceSaveConfirmer.createConfirmedSetItineraryResult({ ok: true }, { date: '2026-06-15' }),
      {
         result: { ok: true },
         diffBaseline: { date: '2026-06-15' },
      }
   );
});

test('Test_GetSetItineraryResultPayload_TestWithAndWithoutItinerary_ExpectPayload', () => {
   const original = ItineraryShape.toSetItineraryPayload;
   ItineraryShape.toSetItineraryPayload = (itinerary) => ({ date: itinerary.date });

   try {
      assert.deepEqual(
         ItineraryServiceSaveConfirmer.getSetItineraryResultPayload({
            itinerary: { date: '2026-06-15' },
         }),
         { date: '2026-06-15' }
      );
      assert.deepEqual(ItineraryServiceSaveConfirmer.getSetItineraryResultPayload({}), {});
   } finally {
      ItineraryShape.toSetItineraryPayload = original;
   }
});

test('Test_RequestSetItineraryConfirmation_TestConfirmAndCancel_ExpectResults', async () => {
   const originalRequest = ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations;
   const originalCancelled = ItineraryConfirmationResult.createItineraryConfirmationCancelledResult;
   let confirmHandler = null;
   let cancelHandler = null;

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
         payload: { date: '2026-06-15' },
         diffBaseline: { base: true },
         buildConfirmedPayload: () => ({ date: '2026-06-15', confirmed: true }),
      });
      await confirmHandler();
      assert.deepEqual(await confirmedPromise, {
         result: {
            confirmed: true,
            payload: { date: '2026-06-15', confirmed: true },
         },
         diffBaseline: { base: true },
      });

      const cancelledPromise = ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
         showConfirmation: ({ onCancel }) => {
            cancelHandler = onCancel;
         },
         initialResult: { issues: ['b'] },
         payload: {},
         diffBaseline: null,
         buildConfirmedPayload: () => ({}),
      });
      cancelHandler();
      assert.deepEqual(await cancelledPromise, { cancelled: true, issues: ['b'] });
   } finally {
      ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = originalRequest;
      ItineraryConfirmationResult.createItineraryConfirmationCancelledResult = originalCancelled;
   }
});

test('Test_RequestSetItineraryWithConfirmations_TestSuccess_ExpectConfirmed', async () => {
   const originalRequest = ItineraryClient.setItineraryRequest;
   const restore = _stubErrorTypeChecks(null);
   ItineraryClient.setItineraryRequest = async () => ({ errorType: 'success', itinerary: {} });

   try {
      assert.deepEqual(
         await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations({ date: '2026-06-15' }, 'base'),
         {
            result: { errorType: 'success', itinerary: {} },
            diffBaseline: 'base',
         }
      );
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
   let shown = null;
   let confirmCalls = 0;

   ItineraryClient.setItineraryRequest = async (payload) => {
      if (payload.overridingConflictingGuardiansTalks) {
         return { errorType: 'success', itinerary: { date: '2026-06-15' } };
      }
      return {
         errorType: 'conflict',
         issues: [{ type: 'conflict' }],
         itinerary: { animals: [{ species: 'Lion' }], attractions: [] },
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
      animals: [{ species: 'Lion' }],
      attractions: [],
   });

   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation;
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

test('Test_RequestSetItineraryWithConfirmations_TestMultiWarnings_ExpectMergedOptions', async () => {
   const originalRequest = ItineraryClient.setItineraryRequest;
   const originalShow = ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation;
   const originalBuild = ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings;
   const restore = _stubErrorTypeChecks('multiWarnings');
   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation;
   let payload = null;

   ItineraryClient.setItineraryRequest = async () => ({
      errorType: 'other',
      issues: [{ type: 'a' }, { type: 'b' }],
   });
   ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation = () => {};
   ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings = () => ({
      confirmingGuardiansTalkUnschedule: true,
      confirmingFixedTimeItemLongWait: true,
   });
   ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation = async (options) => {
      payload = options.buildConfirmedPayload();
      return { result: { errorType: 'success' }, diffBaseline: null };
   };

   try {
      await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations({ date: '2026-06-15' });
      assert.equal(payload.confirmingGuardiansTalkUnschedule, true);
      assert.equal(payload.confirmingFixedTimeItemLongWait, true);
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
   ItineraryClient.setItineraryRequest = async () => ({
      errorType: 'unknown',
      issues: [],
   });

   try {
      assert.deepEqual(
         await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations({ date: '2026-06-15' }, 'base'),
         {
            result: { errorType: 'unknown', issues: [] },
            diffBaseline: 'base',
         }
      );
   } finally {
      ItineraryClient.setItineraryRequest = originalRequest;
      restore();
   }
});
