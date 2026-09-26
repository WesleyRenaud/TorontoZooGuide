import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemResultsBuilder } from '../../../../scripts/itinerary/panel/scheduleItemResultsBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateEmptyState_TestText_ExpectEmptyNode', () => {
   const emptyText = 'No results';

   const empty = ScheduleItemResultsBuilder.createEmptyState(emptyText);

   assert.equal(empty.className, 'itin-empty');
   assert.equal(empty.textContent, emptyText);
});


test('Test_CreateSelectButton_TestUnselected_ExpectAddSymbol', () => {
   const selected = false;

   const { button } = ScheduleItemResultsBuilder.createSelectButton({
      isSelected: () => selected,
      onSelect: () => {},
   });

   assert.equal(button.textContent, Strings.itinerary.actions.addSymbol);
   assert.equal(button.getAttribute('aria-pressed'), String(selected));
});


test('Test_CreateSelectButton_TestSelected_ExpectAddedState', () => {
   let selected = false;
   const { button, updateButtonState } = ScheduleItemResultsBuilder.createSelectButton({
      isSelected: () => selected,
      onSelect: () => {},
   });
   selected = true;

   updateButtonState();

   assert.equal(button.textContent, '✓');
   assert.equal(button.classList.contains('is-added'), selected);
   assert.equal(button.getAttribute('aria-label'), Strings.itinerary.scheduleItem.itemSelected);
});


test('Test_CreateSelectButton_TestClick_ExpectOnSelect', () => {
   const selected = false;
   const selects = [];
   const { button } = ScheduleItemResultsBuilder.createSelectButton({
      isSelected: () => selected,
      onSelect: () => { selects.push(true); },
   });

   button.listeners.click({ stopPropagation() {} });

   assert.deepEqual(selects, [true]);
});


test('Test_CreateResultRow_TestSelected_ExpectPressed', () => {
   const rowId = 'lion';
   const row = { id: rowId };
   const left = document.createElement('div');
   left.className = 'left';

   const item = ScheduleItemResultsBuilder.createResultRow({
      row,
      getId: (nextRow) => nextRow.id,
      selectedRowId: rowId,
      renderRowLeft: () => left,
      onSelectRow: () => {},
   });

   assert.equal(item.classList.contains('is-selected'), true);
   assert.equal(item.getAttribute('aria-pressed'), String(true));
});


test('Test_CreateResultRow_TestClick_ExpectSelectedId', () => {
   const rowId = 'lion';
   const row = { id: rowId };
   const selectedIds = [];
   const left = document.createElement('div');
   left.className = 'left';
   const item = ScheduleItemResultsBuilder.createResultRow({
      row,
      getId: (nextRow) => nextRow.id,
      selectedRowId: rowId,
      renderRowLeft: () => left,
      onSelectRow: (_row, id) => { selectedIds.push(id); },
   });

   item.listeners.click();

   assert.deepEqual(selectedIds, [rowId]);
});


test('Test_CreateResultRow_TestEnterKey_ExpectSelectedId', () => {
   const rowId = 'lion';
   const row = { id: rowId };
   const selectedIds = [];
   const left = document.createElement('div');
   left.className = 'left';
   const item = ScheduleItemResultsBuilder.createResultRow({
      row,
      getId: (nextRow) => nextRow.id,
      selectedRowId: rowId,
      renderRowLeft: () => left,
      onSelectRow: (_row, id) => { selectedIds.push(id); },
   });

   item.listeners.keydown({
      key: 'Enter',
      preventDefault() {},
   });

   assert.deepEqual(selectedIds, [rowId]);
   assert.equal(selectedIds.at(Position.FIRST), row.id);
});
