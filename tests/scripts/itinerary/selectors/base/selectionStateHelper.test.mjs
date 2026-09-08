import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { DraftStore } from '../../../../../scripts/itinerary/draftStore.js';
import { SelectionStateHelper } from '../../../../../scripts/itinerary/selectors/base/selectionStateHelper.js';
import { createLocalStorageMock } from '../../../helpers/localStorageMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});

test('Test_Identity_TestItems_ExpectSameReference', () => {
   const items = [{ id: 'a' }];
   assert.equal(SelectionStateHelper.identity(items), items);
});

test('Test_CloneSelectedItems_TestItems_ExpectShallowCopy', () => {
   const items = [{ id: 'a' }];
   const cloned = SelectionStateHelper.cloneSelectedItems(items);
   assert.deepEqual(cloned, items);
   assert.notEqual(cloned, items);
});

test('Test_LoadAndPersistSelectedItems_TestRoundTrip_ExpectStored', () => {
   SelectionStateHelper.persistSelectedItems('tzg.test', [{ id: 'lion' }]);
   assert.deepEqual(SelectionStateHelper.loadSelectedItems('tzg.test'), [{ id: 'lion' }]);

   const migrated = SelectionStateHelper.loadSelectedItems(
      'tzg.test',
      (items) => items.map((item) => ({ ...item, migrated: true }))
   );
   assert.deepEqual(migrated, [{ id: 'lion', migrated: true }]);
});

test('Test_GetSelectedIndexById_TestMatch_ExpectIndex', () => {
   assert.equal(SelectionStateHelper.getSelectedIndexById([{ id: 'a' }, { id: 'b' }], 'b'), 1);
   assert.equal(SelectionStateHelper.getSelectedIndexById([{ id: 'a' }], 'missing'), -1);
});

test('Test_BuildSelectionItem_TestRow_ExpectMergedId', () => {
   assert.equal(SelectionStateHelper.buildSelectionItem({}, {
      getId: () => '',
      makeSelection: () => ({}),
   }), null);

   assert.deepEqual(SelectionStateHelper.buildSelectionItem({ name: 'Lion' }, {
      getId: (row) => row.name,
      makeSelection: (row) => ({ label: row.name }),
   }), { label: 'Lion', id: 'Lion' });

   assert.deepEqual(SelectionStateHelper.buildSelectionItem({ name: 'Lion' }, {
      getId: (row) => row.name,
      makeSelection: () => null,
   }), { id: 'Lion' });
});

test('Test_LoadSelectedItems_TestUsesDraftStore_ExpectArray', () => {
   DraftStore.saveArray('tzg.selection', [{ id: 'carousel' }]);
   assert.deepEqual(SelectionStateHelper.loadSelectedItems('tzg.selection'), [{ id: 'carousel' }]);
});
