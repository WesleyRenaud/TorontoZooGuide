import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { SelectionStore } from '../../../../../scripts/itinerary/selectors/base/selectionStore.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { createLocalStorageMock } from '../../../helpers/localStorageMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});


test('Test_CreateSelectorSelectionState_TestStoredRow_ExpectSelected', () => {
   const storageKey = 'tzg.test-selection';
   const id = 'lion';
   const name = 'Lion';
   localStorage.setItem(storageKey, JSON.stringify([{ id, name }]));

   const state = SelectionStore.createSelectorSelectionState({
      storageKey,
      getId: (row) => row.id,
      makeSelection: (row) => ({ id: row.id, name: row.name }),
   });

   assert.equal(state.isSelected(id), true);
   assert.equal(state.getSelectedSnapshot().at(Position.FIRST).id, id);
   assert.equal(state.getSelectedSnapshot().at(Position.FIRST).name, name);
});


test('Test_CreateSelectorSelectionState_TestToggleAdd_ExpectAdded', () => {
   const storageKey = 'tzg.test-selection';
   const lionId = 'lion';
   const lionName = 'Lion';
   const tigerId = 'tiger';
   const tigerName = 'Tiger';
   localStorage.setItem(storageKey, JSON.stringify([{ id: lionId, name: lionName }]));
   const state = SelectionStore.createSelectorSelectionState({
      storageKey,
      getId: (row) => row.id,
      makeSelection: (row) => ({ id: row.id, name: row.name }),
   });

   state.toggleRow({ id: tigerId, name: tigerName });

   assert.deepEqual(
      state.getSelectedSnapshot().map((item) => item.id),
      [lionId, tigerId]
   );
});


test('Test_CreateSelectorSelectionState_TestToggleRemove_ExpectRemoved', () => {
   const storageKey = 'tzg.test-selection';
   const lionId = 'lion';
   const lionName = 'Lion';
   const tigerId = 'tiger';
   const tigerName = 'Tiger';
   localStorage.setItem(storageKey, JSON.stringify([{ id: lionId, name: lionName }]));
   const state = SelectionStore.createSelectorSelectionState({
      storageKey,
      getId: (row) => row.id,
      makeSelection: (row) => ({ id: row.id, name: row.name }),
   });
   state.toggleRow({ id: tigerId, name: tigerName });

   state.toggleRow({ id: lionId, name: lionName });

   assert.deepEqual(state.getSelectedSnapshot(), [{ id: tigerId, name: tigerName }]);
   assert.equal(JSON.parse(localStorage.getItem(storageKey)).length, 1);
});


test('Test_CreateSelectorSelectionState_TestMigrate_ExpectNormalized', () => {
   const storageKey = 'tzg.test-selection-migrate';
   const id = 'lion';
   localStorage.setItem(storageKey, JSON.stringify([id]));

   const state = SelectionStore.createSelectorSelectionState({
      storageKey,
      getId: (row) => row.id,
      migrateSelected: (items) => items.map((value) => ({ id: value, name: value })),
   });

   assert.deepEqual(state.getSelectedSnapshot(), [{ id, name: id }]);
});


test('Test_CreateSelectorSelectionState_TestReload_ExpectMigrated', () => {
   const storageKey = 'tzg.test-selection-migrate';
   const firstId = 'lion';
   const nextId = 'tiger';
   localStorage.setItem(storageKey, JSON.stringify([firstId]));
   const state = SelectionStore.createSelectorSelectionState({
      storageKey,
      getId: (row) => row.id,
      migrateSelected: (items) => items.map((value) => ({ id: value, name: value })),
   });
   localStorage.setItem(storageKey, JSON.stringify([nextId]));

   const reloaded = state.reload();

   assert.deepEqual(reloaded, [{ id: nextId, name: nextId }]);
});


test('Test_CreateSelectorSelectionState_TestMissingId_ExpectIgnored', () => {
   const storageKey = 'tzg.test-selection-no-id';
   const state = SelectionStore.createSelectorSelectionState({
      storageKey,
      getId: () => '',
   });

   const selected = state.toggleRow({ name: 'Missing id' });

   assert.deepEqual(selected, []);
   assert.equal(localStorage.getItem(storageKey), null);
});


test('Test_CreateSelectorSelectionState_TestMakeSelectionFallback_ExpectStableId', () => {
   const storageKey = 'tzg.test-selection-fallback';
   const id = 'carousel';
   const state = SelectionStore.createSelectorSelectionState({
      storageKey,
      getId: (row) => row.id,
      makeSelection: () => null,
   });

   state.toggleRow({ id, name: 'Carousel' });

   assert.deepEqual(state.getSelectedSnapshot(), [{ id }]);
});


test('Test_CreateSelectorSelectionState_TestSnapshot_ExpectClone', () => {
   const storageKey = 'tzg.test-selection-clone';
   const id = 'lion';
   const state = SelectionStore.createSelectorSelectionState({
      storageKey,
      getId: (row) => row.id,
   });
   state.toggleRow({ id });

   const snapshot = state.getSelectedSnapshot();
   snapshot.push({ id: 'tiger' });

   assert.deepEqual(state.getSelectedSnapshot(), [{ id }]);
});
