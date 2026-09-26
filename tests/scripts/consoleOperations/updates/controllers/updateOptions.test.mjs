import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { UpdateOptions } from '../../../../../scripts/consoleOperations/updates/controllers/updateOptions.js';
import { UpdateOptionsFormatter } from '../../../../../scripts/consoleOperations/updates/controllers/updateOptionsFormatter.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_LoadActiveUpdates_TestResponse_ExpectUpdatesArray', async () => {
   const updates = [{ title: 'A' }, { title: 'B' }];
   const original = ConsoleOperationsClient.getActiveUpdateOptions;
   ConsoleOperationsClient.getActiveUpdateOptions = async () => ({ updates });

   try {
      const loaded = await UpdateOptions.loadActiveUpdates();

      assert.deepEqual(loaded, updates);
   } finally {
      ConsoleOperationsClient.getActiveUpdateOptions = original;
   }
});


test('Test_LoadActiveUpdates_TestMissingUpdates_ExpectEmptyArray', async () => {
   const original = ConsoleOperationsClient.getActiveUpdateOptions;
   ConsoleOperationsClient.getActiveUpdateOptions = async () => ({});

   try {
      const loaded = await UpdateOptions.loadActiveUpdates();

      assert.deepEqual(loaded, []);
   } finally {
      ConsoleOperationsClient.getActiveUpdateOptions = original;
   }
});


test('Test_PopulateUpdateDropdown_TestDiv_ExpectNoOp', () => {
   const original = UpdateOptionsFormatter.createPlaceholderOption;
   let called = false;
   UpdateOptionsFormatter.createPlaceholderOption = () => {
      called = true;
      return document.createElement('option');
   };

   try {
      UpdateOptions.populateUpdateDropdown(document.createElement('div'), [{ title: 'A' }]);

      assert.equal(called, false);
   } finally {
      UpdateOptionsFormatter.createPlaceholderOption = original;
   }
});


test('Test_PopulateUpdateDropdown_TestNull_ExpectNoOp', () => {
   const original = UpdateOptionsFormatter.createPlaceholderOption;
   let called = false;
   UpdateOptionsFormatter.createPlaceholderOption = () => {
      called = true;
      return document.createElement('option');
   };

   try {
      UpdateOptions.populateUpdateDropdown(null, [{ title: 'A' }]);

      assert.equal(called, false);
   } finally {
      UpdateOptionsFormatter.createPlaceholderOption = original;
   }
});


test('Test_PopulateUpdateDropdown_TestUpdates_ExpectOptions', () => {
   const title = 'Carousel Hours';
   const startDate = '2026-01-01';
   const endDate = '2026-02-01';
   const description = 'Shorter hours';
   const type = 'attraction';
   const update = {
      title,
      start_date: startDate,
      end_date: endDate,
      description,
      type,
   };
   const label = `label:${title}`;
   const selectEl = document.createElement('select');
   const originalLabel = UpdateOptionsFormatter.formatUpdateOptionLabel;
   UpdateOptionsFormatter.formatUpdateOptionLabel = (item) => `label:${item.title}`;

   try {
      UpdateOptions.populateUpdateDropdown(selectEl, [update]);

      const placeholder = selectEl.children.at(Position.FIRST);
      const option = selectEl.children.at(Position.LAST);
      assert.equal(selectEl.children.length, 2);
      assert.equal(placeholder.textContent, Strings.placeholders.update);
      assert.equal(option.textContent, label);
      assert.equal(option.value, JSON.stringify({ title, startDate }));
      assert.equal(option.dataset.title, title);
      assert.equal(option.dataset.startDate, startDate);
      assert.equal(option.dataset.description, description);
      assert.equal(option.dataset.type, type);
      assert.equal(option.dataset.endDate, endDate);
   } finally {
      UpdateOptionsFormatter.formatUpdateOptionLabel = originalLabel;
   }
});


test('Test_GetSelectedUpdateIdentity_TestSelectedOption_ExpectFields', () => {
   const title = 'Notice';
   const startDate = '2026-03-01';
   const option = document.createElement('option');
   option.dataset.title = title;
   option.dataset.startDate = startDate;
   const selectEl = {
      selectedOptions: [option],
   };

   const identity = UpdateOptions.getSelectedUpdateIdentity(selectEl);

   assert.deepEqual(identity, { title, startDate });
});


test('Test_GetSelectedUpdateData_TestSelectedOption_ExpectFields', () => {
   const title = 'Notice';
   const startDate = '2026-03-01';
   const description = 'Desc';
   const type = 'general';
   const endDate = '2026-03-10';
   const option = document.createElement('option');
   option.dataset.title = title;
   option.dataset.startDate = startDate;
   option.dataset.description = description;
   option.dataset.type = type;
   option.dataset.endDate = endDate;
   const selectEl = {
      selectedOptions: [option],
   };

   const data = UpdateOptions.getSelectedUpdateData(selectEl);

   assert.deepEqual(data, {
      title,
      startDate,
      description,
      type,
      endDate,
   });
});


test('Test_GetSelectedUpdateIdentity_TestNull_ExpectEmptyFields', () => {
   const selectEl = null;

   const identity = UpdateOptions.getSelectedUpdateIdentity(selectEl);

   assert.deepEqual(identity, {
      title: '',
      startDate: '',
   });
});
