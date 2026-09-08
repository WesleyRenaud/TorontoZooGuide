import assert from 'node:assert/strict';
import test from 'node:test';

import { UpdateOptions } from '../../../../../scripts/consoleOperations/updates/controllers/updateOptions.js';
import { UpdateOptionsFormatter } from '../../../../../scripts/consoleOperations/updates/controllers/updateOptionsFormatter.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_LoadActiveUpdates_TestResponse_ExpectUpdatesArray', async () => {
   const original = ConsoleOperationsClient.getActiveUpdateOptions;
   ConsoleOperationsClient.getActiveUpdateOptions = async () => ({
      updates: [{ title: 'A' }, { title: 'B' }],
   });

   try {
      assert.deepEqual(await UpdateOptions.loadActiveUpdates(), [
         { title: 'A' },
         { title: 'B' },
      ]);
   } finally {
      ConsoleOperationsClient.getActiveUpdateOptions = original;
   }
});

test('Test_LoadActiveUpdates_TestMissingUpdates_ExpectEmptyArray', async () => {
   const original = ConsoleOperationsClient.getActiveUpdateOptions;
   ConsoleOperationsClient.getActiveUpdateOptions = async () => ({});

   try {
      assert.deepEqual(await UpdateOptions.loadActiveUpdates(), []);
   } finally {
      ConsoleOperationsClient.getActiveUpdateOptions = original;
   }
});

test('Test_PopulateUpdateDropdown_TestNonSelect_ExpectNoOp', () => {
   const original = UpdateOptionsFormatter.createPlaceholderOption;
   let called = false;
   UpdateOptionsFormatter.createPlaceholderOption = () => {
      called = true;
      return document.createElement('option');
   };

   try {
      UpdateOptions.populateUpdateDropdown(document.createElement('div'), [{ title: 'A' }]);
      UpdateOptions.populateUpdateDropdown(null, [{ title: 'A' }]);
      assert.equal(called, false);
   } finally {
      UpdateOptionsFormatter.createPlaceholderOption = original;
   }
});

test('Test_PopulateUpdateDropdown_TestUpdates_ExpectOptions', () => {
   const selectEl = document.createElement('select');
   const originalLabel = UpdateOptionsFormatter.formatUpdateOptionLabel;
   UpdateOptionsFormatter.formatUpdateOptionLabel = (update) => `label:${update.title}`;

   try {
      UpdateOptions.populateUpdateDropdown(selectEl, [
         {
            title: 'Carousel Hours',
            start_date: '2026-01-01',
            end_date: '2026-02-01',
            description: 'Shorter hours',
            type: 'attraction',
         },
      ]);

      assert.equal(selectEl.children.length, 2);
      assert.equal(selectEl.children[0].textContent, Strings.placeholders.update);
      assert.equal(selectEl.children[1].textContent, 'label:Carousel Hours');
      assert.equal(
         selectEl.children[1].value,
         JSON.stringify({ title: 'Carousel Hours', startDate: '2026-01-01' })
      );
      assert.equal(selectEl.children[1].dataset.title, 'Carousel Hours');
      assert.equal(selectEl.children[1].dataset.startDate, '2026-01-01');
      assert.equal(selectEl.children[1].dataset.description, 'Shorter hours');
      assert.equal(selectEl.children[1].dataset.type, 'attraction');
      assert.equal(selectEl.children[1].dataset.endDate, '2026-02-01');
   } finally {
      UpdateOptionsFormatter.formatUpdateOptionLabel = originalLabel;
   }
});

test('Test_GetSelectedUpdateIdentityAndData_TestSelectedOption_ExpectFields', () => {
   const option = document.createElement('option');
   option.dataset.title = 'Notice';
   option.dataset.startDate = '2026-03-01';
   option.dataset.description = 'Desc';
   option.dataset.type = 'general';
   option.dataset.endDate = '2026-03-10';

   const selectEl = {
      selectedOptions: [option],
   };

   assert.deepEqual(UpdateOptions.getSelectedUpdateIdentity(selectEl), {
      title: 'Notice',
      startDate: '2026-03-01',
   });
   assert.deepEqual(UpdateOptions.getSelectedUpdateData(selectEl), {
      title: 'Notice',
      startDate: '2026-03-01',
      description: 'Desc',
      type: 'general',
      endDate: '2026-03-10',
   });
   assert.deepEqual(UpdateOptions.getSelectedUpdateIdentity(null), {
      title: '',
      startDate: '',
   });
});
