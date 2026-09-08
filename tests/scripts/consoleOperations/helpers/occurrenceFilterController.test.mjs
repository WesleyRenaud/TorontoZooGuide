import assert from 'node:assert/strict';
import test from 'node:test';

import { OccurrenceFilterController } from '../../../../scripts/consoleOperations/helpers/occurrenceFilterController.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateOccurrenceFilterController_TestSingleTime_ExpectAutoSelect', async () => {
   const dateEl = document.createElement('select');
   const timeEl = document.createElement('select');

   dateEl.appendChild(document.createElement('option'));
   timeEl.appendChild(document.createElement('option'));

   const controller = OccurrenceFilterController.createOccurrenceFilterController({
      dateEl,
      timeEl,
      autoSelectSingleTime: true,
      getSelectionValues: () => ({
         talk: 'African Lion',
         location: 'Africa Savanna',
      }),
      isSelectionReady: () => true,
      loadOccurrences: async () => ([
         { date: '2026-06-15', time: '10:00 AM' },
      ]),
   });

   await controller.refresh();
   dateEl.value = '2026-06-15';
   controller.refreshTimes();

   assert.equal(timeEl.value, '10:00 AM');
});

test('Test_CreateOccurrenceFilterController_TestCustomPopulateNotReadyErrorAndEmptyDate_ExpectGuards', async () => {
   const dateEl = document.createElement('select');
   const timeEl = document.createElement('select');
   const populatedTimes = [];
   let ready = false;

   dateEl.appendChild(document.createElement('option'));
   timeEl.appendChild(document.createElement('option'));

   const controller = OccurrenceFilterController.createOccurrenceFilterController({
      dateEl,
      timeEl,
      populateTimes: (times) => {
         populatedTimes.push([...times]);
      },
      getSelectionValues: () => ({ talk: 'Lion' }),
      isSelectionReady: () => ready,
      loadOccurrences: async () => {
         throw new Error('load failed');
      },
   });

   await controller.refresh();
   assert.deepEqual(populatedTimes.at(-1), []);

   ready = true;
   await controller.refresh();
   assert.deepEqual(populatedTimes.at(-1), []);

   dateEl.value = '';
   const beforeEmptyDate = populatedTimes.length;
   controller.refreshTimes();
   assert.equal(populatedTimes.length, beforeEmptyDate + 1);
   assert.deepEqual(populatedTimes.at(-1), []);
});
