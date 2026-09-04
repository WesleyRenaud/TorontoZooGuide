import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { SelectionState } from '../../../../../scripts/itinerary/selectors/base/selectionState.js';
import { createLocalStorageMock } from '../../../helpers/localStorageMock.mjs';

test.describe('Test_CreateSelectorSelectionState', () => {
   beforeEach(() => {
      globalThis.localStorage = createLocalStorageMock();
   });

   afterEach(() => {
      delete globalThis.localStorage;
   });

   test('Test_CreateSelectorSelectionState_TestToggle_ExpectOnOff', () => {
      localStorage.setItem(
         'tzg.test-selection',
         JSON.stringify([{ id: 'lion', name: 'Lion' }])
      );

      const state = SelectionState.createSelectorSelectionState({
         storageKey: 'tzg.test-selection',
         getId: (row) => row.id,
         makeSelection: (row) => ({ id: row.id, name: row.name }),
      });

      assert.equal(state.isSelected('lion'), true);
      assert.deepEqual(state.getSelectedSnapshot(), [{ id: 'lion', name: 'Lion' }]);

      state.toggleRow({ id: 'tiger', name: 'Tiger' });
      assert.deepEqual(
         state.getSelectedSnapshot().map((item) => item.id),
         ['lion', 'tiger']
      );

      state.toggleRow({ id: 'lion', name: 'Lion' });
      assert.deepEqual(state.getSelectedSnapshot(), [{ id: 'tiger', name: 'Tiger' }]);
      assert.equal(
         JSON.parse(localStorage.getItem('tzg.test-selection')).length,
         1
      );
   });

   test('Test_CreateSelectorSelectionState_TestMigrate_ExpectNormalized', () => {
      localStorage.setItem(
         'tzg.test-selection-migrate',
         JSON.stringify(['lion'])
      );

      const state = SelectionState.createSelectorSelectionState({
         storageKey: 'tzg.test-selection-migrate',
         getId: (row) => row.id,
         migrateSelected: (items) => items.map((id) => ({ id, name: id })),
      });

      assert.deepEqual(state.getSelectedSnapshot(), [{ id: 'lion', name: 'lion' }]);

      localStorage.setItem(
         'tzg.test-selection-migrate',
         JSON.stringify(['tiger'])
      );

      assert.deepEqual(state.reload(), [{ id: 'tiger', name: 'tiger' }]);
   });

   test('Test_CreateSelectorSelectionState_TestMissingId_ExpectIgnored', () => {
      const state = SelectionState.createSelectorSelectionState({
         storageKey: 'tzg.test-selection-no-id',
         getId: () => '',
      });

      assert.deepEqual(state.toggleRow({ name: 'Missing id' }), []);
      assert.equal(localStorage.getItem('tzg.test-selection-no-id'), null);
   });

   test('Test_CreateSelectorSelectionState_TestMakeSelectionFallback_ExpectStableId', () => {
      const state = SelectionState.createSelectorSelectionState({
         storageKey: 'tzg.test-selection-fallback',
         getId: (row) => row.id,
         makeSelection: () => null,
      });

      state.toggleRow({ id: 'carousel', name: 'Carousel' });

      assert.deepEqual(state.getSelectedSnapshot(), [{ id: 'carousel' }]);
   });

   test('Test_CreateSelectorSelectionState_TestSnapshot_ExpectClone', () => {
      const state = SelectionState.createSelectorSelectionState({
         storageKey: 'tzg.test-selection-clone',
         getId: (row) => row.id,
      });

      state.toggleRow({ id: 'lion' });

      const snapshot = state.getSelectedSnapshot();
      snapshot.push({ id: 'tiger' });

      assert.deepEqual(state.getSelectedSnapshot(), [{ id: 'lion' }]);
   });
});
