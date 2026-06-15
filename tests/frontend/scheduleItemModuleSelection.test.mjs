import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   canScheduleModuleSelection,
   filterVisibleScheduleModuleRows,
   resolveScheduleModuleSearchLabel,
   shouldClearSelectedScheduleRow,
} from '../../scripts/itinerary/panel/components/scheduleItemModuleSelection.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';

const EVENT_TYPES = ['lunch', 'break'];

const ANIMAL_ROW = {
   species: 'Tiger',
   exhibit: 'Savanna',
   scheduleItemKind: 'animals',
};

const ATTRACTION_ROW = {
   name: 'Carousel',
   scheduleItemKind: 'attractions',
};

test('canScheduleModuleSelection requires a row for searchable kinds', () => {
   assert.equal(
      canScheduleModuleSelection({
         selection: ScheduleItemKind.ANIMAL.itemType,
         selectedRow: null,
         eventTypes: EVENT_TYPES,
      }),
      false
   );
   assert.equal(
      canScheduleModuleSelection({
         selection: ScheduleItemKind.ANIMAL.itemType,
         selectedRow: ANIMAL_ROW,
         eventTypes: EVENT_TYPES,
      }),
      true
   );
});

test('canScheduleModuleSelection allows event types without a selected row', () => {
   assert.equal(
      canScheduleModuleSelection({
         selection: 'lunch',
         selectedRow: null,
         eventTypes: EVENT_TYPES,
      }),
      true
   );
   assert.equal(
      canScheduleModuleSelection({
         selection: '',
         selectedRow: null,
         eventTypes: EVENT_TYPES,
      }),
      false
   );
});

test('filterVisibleScheduleModuleRows keeps itinerary rows when the filter is enabled', () => {
   const rows = [ANIMAL_ROW, ATTRACTION_ROW];

   assert.deepEqual(
      filterVisibleScheduleModuleRows({
         rows,
         itinerary: {
            animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
            attractions: [],
         },
         onlyItineraryItemsEnabled: true,
      }),
      [ANIMAL_ROW]
   );
   assert.deepEqual(
      filterVisibleScheduleModuleRows({
         rows,
         onlyItineraryItemsEnabled: false,
      }),
      rows
   );
});

test('shouldClearSelectedScheduleRow detects filtered-out selections', () => {
   assert.equal(
      shouldClearSelectedScheduleRow({
         selectedRowId: 'Tiger||Savanna',
         visibleRows: [ATTRACTION_ROW],
      }),
      true
   );
   assert.equal(
      shouldClearSelectedScheduleRow({
         selectedRowId: 'Tiger||Savanna',
         visibleRows: [ANIMAL_ROW],
      }),
      false
   );
});

test('resolveScheduleModuleSearchLabel uses species or attraction titles', () => {
   assert.equal(resolveScheduleModuleSearchLabel(ANIMAL_ROW), 'Tiger');
   assert.equal(resolveScheduleModuleSearchLabel(ATTRACTION_ROW), 'Carousel');
});
