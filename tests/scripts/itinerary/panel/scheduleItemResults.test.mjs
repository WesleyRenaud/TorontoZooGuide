import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ScheduleItemResults } from '../../../../scripts/itinerary/panel/scheduleItemResults.js';
import { ScheduleItemKeySeparator } from '../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import {
   createDomNode,
   installDocument,
   teardownDocument,
} from '../../helpers/domMock.mjs';

function _findSelectButton(row) {
   return row.children.find((child) => (
      child.className?.includes('schedule-item-select-btn')
   ));
}

function _createSingleSelectHandler() {
   let selectedRowId = '';

   return {
      getSelectedRowId: () => selectedRowId,
      onSelectRow(_row, id) {
         selectedRowId = selectedRowId === id ? '' : id;
      },
   };
}

function _renderRows(resultsEl, rows, selection) {
   ScheduleItemResults.renderScheduleItemSearchResults({
      resultsEl,
      rows,
      emptyText: 'No matching items',
      getId: (row) => (
         row.species
            ? [row.species, row.exhibit].join(ScheduleItemKeySeparator.VALUE)
            : row.name
      ),
      selectedRowId: selection.getSelectedRowId(),
      renderRowLeft: () => createDomNode('div', 'row-left'),
      onSelectRow: (row, id) => {
         selection.onSelectRow(row, id);
         _renderRows(resultsEl, rows, selection);
      },
   });
}

afterEach(() => {
   teardownDocument();
});


test('Test_RenderScheduleItemSearchResults_TestNoRows_ExpectEmptyState', () => {
   installDocument();
   const emptyText = 'No matching items';
   const resultsEl = createDomNode('div', 'schedule-item-results');

   ScheduleItemResults.renderScheduleItemSearchResults({
      resultsEl,
      rows: [],
      emptyText,
      getId: () => 'id',
      renderRowLeft: () => createDomNode('div'),
      onSelectRow: () => {},
   });

   assert.equal(resultsEl.children.at(Position.FIRST).textContent, emptyText);
});


test('Test_RenderScheduleItemSearchResults_TestMissingResultsEl_ExpectNoOp', () => {
   assert.doesNotThrow(() => {
      ScheduleItemResults.renderScheduleItemSearchResults({
         resultsEl: null,
         rows: [{ name: 'Conservation Carousel' }],
      });
   });
});


test('Test_RenderScheduleItemSearchResults_TestSelectedRow_ExpectMarked', () => {
   installDocument();
   const species = 'Amur Tiger';
   const exhibit = 'Eurasia Wilds';
   const resultsEl = createDomNode('div', 'schedule-item-results');
   const rows = [{ species, exhibit }];
   const selection = _createSingleSelectHandler();

   _renderRows(resultsEl, rows, selection);
   resultsEl.children.at(Position.FIRST).listeners.click();

   const activeRow = resultsEl.children.at(Position.FIRST);

   assert.equal(
      selection.getSelectedRowId(),
      [species, exhibit].join(ScheduleItemKeySeparator.VALUE)
   );
   assert.equal(activeRow.getAttribute('aria-pressed'), String(true));
   assert.match(_findSelectButton(activeRow).className, /is-added/);
});


test('Test_RenderScheduleItemSearchResults_TestReselectSame_ExpectCleared', () => {
   installDocument();
   const species = 'Amur Tiger';
   const exhibit = 'Eurasia Wilds';
   const resultsEl = createDomNode('div', 'schedule-item-results');
   const rows = [{ species, exhibit }];
   const selection = _createSingleSelectHandler();

   _renderRows(resultsEl, rows, selection);
   resultsEl.children.at(Position.FIRST).listeners.click();
   resultsEl.children.at(Position.FIRST).listeners.click();

   assert.equal(selection.getSelectedRowId(), '');
   assert.equal(resultsEl.children.at(Position.FIRST).getAttribute('aria-pressed'), String(false));
});


test('Test_RenderScheduleItemSearchResults_TestKeyboard_ExpectSelected', () => {
   installDocument();
   const name = 'Conservation Carousel';
   const resultsEl = createDomNode('div', 'schedule-item-results');
   const selection = _createSingleSelectHandler();

   ScheduleItemResults.renderScheduleItemSearchResults({
      resultsEl,
      rows: [{ name }],
      emptyText: 'No matching items',
      getId: () => name,
      selectedRowId: selection.getSelectedRowId(),
      renderRowLeft: () => createDomNode('div'),
      onSelectRow: selection.onSelectRow,
   });
   resultsEl.children.at(Position.FIRST).listeners.keydown({
      key: 'Enter',
      preventDefault() {},
   });

   assert.equal(selection.getSelectedRowId(), name);
});
