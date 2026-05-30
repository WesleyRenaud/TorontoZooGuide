import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { renderScheduleItemSearchResults } from '../../scripts/itinerary/panel/scheduleItemResults.js';
import {
   createDomNode,
   installDocument,
   teardownDocument,
} from './helpers/domMock.mjs';

afterEach(() => {
   teardownDocument();
});

function findSelectButton(row) {
   return row.children.find((child) => (
      child.className?.includes('schedule-item-select-btn')
   ));
}

function createSingleSelectHandler() {
   let selectedRowId = '';

   return {
      getSelectedRowId: () => selectedRowId,
      onSelectRow(_row, id) {
         selectedRowId = selectedRowId === id ? '' : id;
      },
   };
}

test('renderScheduleItemSearchResults shows an empty state when there are no rows', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'schedule-item-results');

   renderScheduleItemSearchResults({
      resultsEl,
      rows: [],
      emptyText: 'No matching items',
      getId: () => 'id',
      renderRowLeft: () => createDomNode('div'),
      onSelectRow: () => {},
   });

   assert.equal(resultsEl.children[0].textContent, 'No matching items');
});

function renderRows(resultsEl, rows, selection) {
   renderScheduleItemSearchResults({
      resultsEl,
      rows,
      emptyText: 'No matching items',
      getId: (row) => (
         row.species ? `${row.species}||${row.exhibit}` : row.name
      ),
      selectedRowId: selection.getSelectedRowId(),
      renderRowLeft: () => createDomNode('div', 'row-left'),
      onSelectRow: (row, id) => {
         selection.onSelectRow(row, id);
         renderRows(resultsEl, rows, selection);
      },
   });
}

test('renderScheduleItemSearchResults marks the selected row and + control', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'schedule-item-results');
   const rows = [{ species: 'Tiger', exhibit: 'Savanna' }];
   const selection = createSingleSelectHandler();

   renderRows(resultsEl, rows, selection);
   resultsEl.children[0].listeners.click();

   const activeRow = resultsEl.children[0];
   assert.equal(selection.getSelectedRowId(), 'Tiger||Savanna');
   assert.equal(activeRow.getAttribute('aria-pressed'), 'true');
   assert.match(findSelectButton(activeRow).className, /is-added/);
});

test('renderScheduleItemSearchResults clears selection when the same row is chosen again', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'schedule-item-results');
   const rows = [{ species: 'Tiger', exhibit: 'Savanna' }];
   const selection = createSingleSelectHandler();

   renderRows(resultsEl, rows, selection);
   resultsEl.children[0].listeners.click();
   resultsEl.children[0].listeners.click();

   assert.equal(selection.getSelectedRowId(), '');
   assert.equal(resultsEl.children[0].getAttribute('aria-pressed'), 'false');
});

test('renderScheduleItemSearchResults supports keyboard selection', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'schedule-item-results');
   const selection = createSingleSelectHandler();

   renderScheduleItemSearchResults({
      resultsEl,
      rows: [{ name: 'Carousel' }],
      emptyText: 'No matching items',
      getId: () => 'Carousel',
      selectedRowId: selection.getSelectedRowId(),
      renderRowLeft: () => createDomNode('div'),
      onSelectRow: selection.onSelectRow,
   });

   resultsEl.children[0].listeners.keydown({
      key: 'Enter',
      preventDefault() {},
   });

   assert.equal(selection.getSelectedRowId(), 'Carousel');
});
