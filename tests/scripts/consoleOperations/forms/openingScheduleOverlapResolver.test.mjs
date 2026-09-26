import assert from 'node:assert/strict';
import test from 'node:test';

import { OpeningScheduleOverlapResolver } from '../../../../scripts/consoleOperations/forms/openingScheduleOverlapResolver.js';
import { OpeningScheduleOverlapResolution } from '../../../../scripts/shared/enums/openingScheduleOverlapResolution.js';

const RESTAURANT = 'Peaks';
const PAYLOAD = { restaurant: RESTAURANT };


test('Test_ResolveOpeningScheduleOverlapConflict_TestReplace_ExpectReplaceCallback', async () => {
   const replaced = { replaced: PAYLOAD };
   let replaceCalled = false;

   const result = await OpeningScheduleOverlapResolver.resolveOpeningScheduleOverlapConflict({
      payload: PAYLOAD,
      replaceOverlaps: async (payload) => {
         replaceCalled = true;
         return { replaced: payload };
      },
      trimOverlaps: async () => ({ trimmed: true }),
      showDialog: async () => OpeningScheduleOverlapResolution.REPLACE,
   });

   assert.equal(replaceCalled, true);
   assert.deepEqual(result, replaced);
});


test('Test_ResolveOpeningScheduleOverlapConflict_TestTrim_ExpectTrimCallback', async () => {
   const trimmed = { trimmed: PAYLOAD };
   let trimCalled = false;

   const result = await OpeningScheduleOverlapResolver.resolveOpeningScheduleOverlapConflict({
      payload: PAYLOAD,
      replaceOverlaps: async () => ({ replaced: true }),
      trimOverlaps: async (payload) => {
         trimCalled = true;
         return { trimmed: payload };
      },
      showDialog: async () => OpeningScheduleOverlapResolution.TRIM,
   });

   assert.equal(trimCalled, true);
   assert.deepEqual(result, trimmed);
});


test('Test_ResolveOpeningScheduleOverlapConflict_TestDismiss_ExpectDismissedResult', async () => {
   const dismissedResult = { success: false, dismissed: true };

   const result = await OpeningScheduleOverlapResolver.resolveOpeningScheduleOverlapConflict({
      payload: PAYLOAD,
      replaceOverlaps: async () => ({ replaced: true }),
      trimOverlaps: async () => ({ trimmed: true }),
      dismissedResult,
      showDialog: async () => null,
   });

   assert.deepEqual(result, dismissedResult);
});


test('Test_ResolveOpeningScheduleOverlapConflict_TestDismissWithoutResult_ExpectNull', async () => {
   const result = await OpeningScheduleOverlapResolver.resolveOpeningScheduleOverlapConflict({
      payload: PAYLOAD,
      replaceOverlaps: async () => ({ replaced: true }),
      trimOverlaps: async () => ({ trimmed: true }),
      showDialog: async () => null,
   });

   assert.equal(result, null);
});
