import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemResultsBuilder } from '../../../../scripts/itinerary/panel/scheduleItemResultsBuilder.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEmptyState_TestText_ExpectEmptyNode', () => {
   const empty = ScheduleItemResultsBuilder.createEmptyState('No results');
   assert.equal(empty.className, 'itin-empty');
   assert.equal(empty.textContent, 'No results');
});

test('Test_CreateSelectButton_TestToggle_ExpectSelectedState', () => {
   let selected = false;
   const selects = [];
   const { button, updateButtonState } = ScheduleItemResultsBuilder.createSelectButton({
      isSelected: () => selected,
      onSelect: () => { selects.push(true); },
   });

   assert.equal(button.textContent, Strings.itinerary.actions.addSymbol);
   assert.equal(button.getAttribute('aria-pressed'), 'false');

   selected = true;
   updateButtonState();
   assert.equal(button.textContent, '✓');
   assert.equal(button.classList.contains('is-added'), true);
   assert.equal(button.getAttribute('aria-label'), Strings.itinerary.scheduleItem.itemSelected);

   button.listeners.click({ stopPropagation() {} });
   assert.deepEqual(selects, [true]);
});

test('Test_CreateResultRow_TestSelect_ExpectHandlers', () => {
   const selectedIds = [];
   const left = document.createElement('div');
   left.className = 'left';

   const item = ScheduleItemResultsBuilder.createResultRow({
      row: { id: 'lion' },
      getId: (row) => row.id,
      selectedRowId: 'lion',
      renderRowLeft: () => left,
      onSelectRow: (_row, id) => { selectedIds.push(id); },
   });

   assert.equal(item.classList.contains('is-selected'), true);
   assert.equal(item.getAttribute('aria-pressed'), 'true');
   item.listeners.click();
   assert.deepEqual(selectedIds, ['lion']);

   item.listeners.keydown({
      key: 'Enter',
      preventDefault() {},
   });
   assert.deepEqual(selectedIds, ['lion', 'lion']);
});
