import assert from 'node:assert/strict';
import test from 'node:test';

import { OccurrenceFilterController } from '../../../../scripts/consoleOperations/helpers/occurrenceFilterController.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateOccurrenceFilterController_TestSingleTime_ExpectAutoSelect', async () => {
   const date = '2026-06-15';
   const time = '10:00 AM';
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
         { date, time },
      ]),
   });
   await controller.refresh();
   dateEl.value = date;
   controller.refreshTimes();

   assert.equal(timeEl.value, time);
});


test('Test_CreateOccurrenceFilterController_TestNotReady_ExpectEmptyTimes', async () => {
   const dateEl = document.createElement('select');
   const timeEl = document.createElement('select');
   const populatedTimes = [];
   dateEl.appendChild(document.createElement('option'));
   timeEl.appendChild(document.createElement('option'));

   const controller = OccurrenceFilterController.createOccurrenceFilterController({
      dateEl,
      timeEl,
      populateTimes: (times) => {
         populatedTimes.push([...times]);
      },
      getSelectionValues: () => ({ talk: 'Lion' }),
      isSelectionReady: () => false,
      loadOccurrences: async () => {
         throw new Error('load failed');
      },
   });
   await controller.refresh();

   assert.deepEqual(populatedTimes.at(Position.LAST), []);
});


test('Test_CreateOccurrenceFilterController_TestLoadError_ExpectEmptyTimes', async () => {
   const dateEl = document.createElement('select');
   const timeEl = document.createElement('select');
   const populatedTimes = [];
   dateEl.appendChild(document.createElement('option'));
   timeEl.appendChild(document.createElement('option'));

   const controller = OccurrenceFilterController.createOccurrenceFilterController({
      dateEl,
      timeEl,
      populateTimes: (times) => {
         populatedTimes.push([...times]);
      },
      getSelectionValues: () => ({ talk: 'Lion' }),
      isSelectionReady: () => true,
      loadOccurrences: async () => {
         throw new Error('load failed');
      },
   });
   await controller.refresh();

   assert.deepEqual(populatedTimes.at(Position.LAST), []);
});


test('Test_CreateOccurrenceFilterController_TestEmptyDate_ExpectEmptyTimes', async () => {
   const dateEl = document.createElement('select');
   const timeEl = document.createElement('select');
   const populatedTimes = [];
   dateEl.appendChild(document.createElement('option'));
   timeEl.appendChild(document.createElement('option'));

   const controller = OccurrenceFilterController.createOccurrenceFilterController({
      dateEl,
      timeEl,
      populateTimes: (times) => {
         populatedTimes.push([...times]);
      },
      getSelectionValues: () => ({ talk: 'Lion' }),
      isSelectionReady: () => true,
      loadOccurrences: async () => [],
   });
   await controller.refresh();
   dateEl.value = '';
   const beforeEmptyDate = populatedTimes.length;
   controller.refreshTimes();

   assert.equal(populatedTimes.length, beforeEmptyDate + 1);
   assert.deepEqual(populatedTimes.at(Position.LAST), []);
});
