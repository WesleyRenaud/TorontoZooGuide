import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { DraftStore } from '../../../../../scripts/itinerary/draftStore.js';
import { SelectionStateHelper } from '../../../../../scripts/itinerary/selectors/base/selectionStateHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { createLocalStorageMock } from '../../../helpers/localStorageMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});


test('Test_Identity_TestItems_ExpectSameReference', () => {
   const items = [{ id: 'a' }];

   const identity = SelectionStateHelper.identity(items);

   assert.equal(identity, items);
});


test('Test_CloneSelectedItems_TestItems_ExpectShallowCopy', () => {
   const items = [{ id: 'a' }];

   const cloned = SelectionStateHelper.cloneSelectedItems(items);

   assert.deepEqual(cloned, items);
   assert.notEqual(cloned, items);
});


test('Test_PersistSelectedItems_TestItems_ExpectStored', () => {
   const storageKey = 'tzg.test';
   const items = [{ id: 'lion' }];

   SelectionStateHelper.persistSelectedItems(storageKey, items);

   assert.deepEqual(SelectionStateHelper.loadSelectedItems(storageKey), items);
});


test('Test_LoadSelectedItems_TestMigrate_ExpectNormalized', () => {
   const storageKey = 'tzg.test';
   const id = 'lion';
   SelectionStateHelper.persistSelectedItems(storageKey, [{ id }]);

   const migrated = SelectionStateHelper.loadSelectedItems(
      storageKey,
      (items) => items.map((item) => ({ ...item, migrated: true }))
   );

   assert.equal(migrated.at(Position.FIRST).id, id);
   assert.equal(migrated.at(Position.FIRST).migrated, true);
});


test('Test_GetSelectedIndexById_TestMatch_ExpectIndex', () => {
   const firstId = 'a';
   const secondId = 'b';
   const items = [{ id: firstId }, { id: secondId }];

   const index = SelectionStateHelper.getSelectedIndexById(items, secondId);

   assert.equal(index, Position.SECOND);
});


test('Test_GetSelectedIndexById_TestMissing_ExpectLast', () => {
   const firstId = 'a';
   const missingId = 'missing';
   const items = [{ id: firstId }];

   const index = SelectionStateHelper.getSelectedIndexById(items, missingId);

   assert.equal(index, Position.LAST);
});


test('Test_BuildSelectionItem_TestMissingId_ExpectNull', () => {
   const row = {};

   const item = SelectionStateHelper.buildSelectionItem(row, {
      getId: () => '',
      makeSelection: () => ({}),
   });

   assert.equal(item, null);
});


test('Test_BuildSelectionItem_TestRow_ExpectMergedId', () => {
   const name = 'Lion';
   const row = { name };

   const item = SelectionStateHelper.buildSelectionItem(row, {
      getId: (value) => value.name,
      makeSelection: (value) => ({ label: value.name }),
   });

   assert.equal(item.label, name);
   assert.equal(item.id, name);
});


test('Test_BuildSelectionItem_TestNullSelection_ExpectIdOnly', () => {
   const name = 'Lion';
   const row = { name };

   const item = SelectionStateHelper.buildSelectionItem(row, {
      getId: (value) => value.name,
      makeSelection: () => null,
   });

   assert.equal(item.id, name);
});


test('Test_LoadSelectedItems_TestUsesDraftStore_ExpectArray', () => {
   const storageKey = 'tzg.selection';
   const items = [{ id: 'carousel' }];
   DraftStore.saveArray(storageKey, items);

   const loaded = SelectionStateHelper.loadSelectedItems(storageKey);

   assert.deepEqual(loaded, items);
});
