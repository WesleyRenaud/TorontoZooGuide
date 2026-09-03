import assert from 'node:assert/strict';
import test from 'node:test';

import { createOccurrenceFilterController } from '../../scripts/consoleOperations/helpers/occurrenceFilterController.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

test.describe('occurrence filter controller', () => {
   installDomTestHooks();

   test('refreshTimes auto-selects a single time in the dropdown', async () => {
      const dateEl = document.createElement('select');
      const timeEl = document.createElement('select');

      dateEl.appendChild(document.createElement('option'));
      timeEl.appendChild(document.createElement('option'));

      const controller = createOccurrenceFilterController({
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
});
