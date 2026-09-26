import assert from 'node:assert/strict';
import test from 'node:test';

import { UpdateOptionsFormatter } from '../../../../../scripts/consoleOperations/updates/controllers/updateOptionsFormatter.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreatePlaceholderOption_TestLabel_ExpectEmptyValueOption', () => {
   const label = 'Select an update';

   const optionEl = UpdateOptionsFormatter.createPlaceholderOption(label);

   assert.equal(optionEl.tagName, 'OPTION');
   assert.equal(optionEl.value, '');
   assert.equal(optionEl.textContent, label);
});


test('Test_FormatDateRange_TestOpenEnded_ExpectOnward', () => {
   const startDate = '2026-01-01';
   const update = { start_date: startDate };

   const formatted = UpdateOptionsFormatter.formatDateRange(update);

   assert.equal(formatted, Strings.format.dateOnward(startDate));
});


test('Test_FormatDateRange_TestClosedRange_ExpectTo', () => {
   const startDate = '2026-01-01';
   const endDate = '2026-02-01';
   const update = {
      start_date: startDate,
      end_date: endDate,
   };

   const formatted = UpdateOptionsFormatter.formatDateRange(update);

   assert.equal(formatted, Strings.format.dateRangeTo(startDate, endDate));
});


test('Test_FormatUpdateOptionLabel_TestUpdate_ExpectCombinedLabel', () => {
   const title = 'Carousel Hours';
   const type = 'attraction';
   const startDate = '2026-01-01';
   const endDate = '2026-02-01';
   const update = {
      title,
      type,
      start_date: startDate,
      end_date: endDate,
   };

   const label = UpdateOptionsFormatter.formatUpdateOptionLabel(update);

   assert.equal(
      label,
      `${title} (${type}, ${UpdateOptionsFormatter.formatDateRange(update)})`
   );
});
