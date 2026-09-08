import assert from 'node:assert/strict';
import test from 'node:test';

import { UpdateOptionsFormatter } from '../../../../../scripts/consoleOperations/updates/controllers/updateOptionsFormatter.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreatePlaceholderOption_TestLabel_ExpectEmptyValueOption', () => {
   const optionEl = UpdateOptionsFormatter.createPlaceholderOption('Select an update');

   assert.equal(optionEl.tagName, 'OPTION');
   assert.equal(optionEl.value, '');
   assert.equal(optionEl.textContent, 'Select an update');
});

test('Test_FormatDateRange_TestOpenEnded_ExpectOnward', () => {
   assert.equal(
      UpdateOptionsFormatter.formatDateRange({ start_date: '2026-01-01' }),
      '2026-01-01 onward'
   );
});

test('Test_FormatDateRange_TestClosedRange_ExpectTo', () => {
   assert.equal(
      UpdateOptionsFormatter.formatDateRange({
         start_date: '2026-01-01',
         end_date: '2026-02-01',
      }),
      '2026-01-01 to 2026-02-01'
   );
});

test('Test_FormatUpdateOptionLabel_TestUpdate_ExpectCombinedLabel', () => {
   assert.equal(
      UpdateOptionsFormatter.formatUpdateOptionLabel({
         title: 'Carousel Hours',
         type: 'attraction',
         start_date: '2026-01-01',
         end_date: '2026-02-01',
      }),
      'Carousel Hours (attraction, 2026-01-01 to 2026-02-01)'
   );
});
