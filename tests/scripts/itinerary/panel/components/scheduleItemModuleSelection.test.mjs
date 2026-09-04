import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemModuleSelection } from '../../../../../scripts/itinerary/panel/components/scheduleItemModuleSelection.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';

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

const GUARDIANS_TALK_ROW = {
   name: 'Amur Tiger',
   start_time: '1:30 PM',
   scheduleItemKind: 'guardians_talks',
};

const WILD_ENCOUNTER_ROW = {
   name: 'African Rainforest',
   start_time: '2:00 PM',
   scheduleItemKind: 'wild_encounters',
};

const TRANSPORTATION_ROW = {
   name: 'Zoomobile',
   added_as_attraction: false,
   scheduleItemKind: 'transportations',
};

const ZOOMOBILE_AS_ATTRACTION_ROW = {
   name: 'Zoomobile',
   added_as_attraction: true,
   scheduleItemKind: 'attractions',
};

test('Test_CanScheduleModuleSelection_TestSearchableKinds_ExpectRowRequired', () => {
   assert.equal(
      ScheduleItemModuleSelection.canScheduleModuleSelection({
         selection: ScheduleItemKind.ANIMAL.itemType,
         selectedRow: null,
         eventTypes: EVENT_TYPES,
      }),
      false
   );
   assert.equal(
      ScheduleItemModuleSelection.canScheduleModuleSelection({
         selection: ScheduleItemKind.ANIMAL.itemType,
         selectedRow: ANIMAL_ROW,
         eventTypes: EVENT_TYPES,
      }),
      true
   );
});

test('Test_CanScheduleModuleSelection_TestTransportationAttraction_ExpectAllowed', () => {
   assert.equal(
      ScheduleItemModuleSelection.canScheduleModuleSelection({
         selection: ScheduleItemKind.ATTRACTION.itemType,
         selectedRow: ZOOMOBILE_AS_ATTRACTION_ROW,
         eventTypes: EVENT_TYPES,
      }),
      true
   );
   assert.equal(
      ScheduleItemModuleSelection.canScheduleModuleSelection({
         selection: ScheduleItemKind.TRANSPORTATION.itemType,
         selectedRow: TRANSPORTATION_ROW,
         eventTypes: EVENT_TYPES,
      }),
      true
   );
});

test('Test_CanScheduleModuleSelection_TestEventTypes_ExpectNoRowRequired', () => {
   assert.equal(
      ScheduleItemModuleSelection.canScheduleModuleSelection({
         selection: 'lunch',
         selectedRow: null,
         eventTypes: EVENT_TYPES,
      }),
      true
   );
   assert.equal(
      ScheduleItemModuleSelection.canScheduleModuleSelection({
         selection: '',
         selectedRow: null,
         eventTypes: EVENT_TYPES,
      }),
      false
   );
});

test('Test_FilterVisibleScheduleModuleRows_TestItineraryFilter_ExpectKeepsItineraryRows', () => {
   const rows = [ANIMAL_ROW, ATTRACTION_ROW];

   assert.deepEqual(
      ScheduleItemModuleSelection.filterVisibleScheduleModuleRows({
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
      ScheduleItemModuleSelection.filterVisibleScheduleModuleRows({
         rows,
         onlyItineraryItemsEnabled: false,
      }),
      rows
   );
});

test('Test_FilterVisibleScheduleModuleRows_TestScheduledTalks_ExpectHidden', () => {
   const rows = [ANIMAL_ROW, GUARDIANS_TALK_ROW, WILD_ENCOUNTER_ROW];
   const itinerary = {
      animals: [],
      guardiansTalks: [{ name: 'Amur Tiger', start_time: '1:30 PM' }],
      wildEncounters: [{ name: 'African Rainforest', start_time: '2:00 PM' }],
   };

   assert.deepEqual(
      ScheduleItemModuleSelection.filterVisibleScheduleModuleRows({
         rows,
         itinerary,
         onlyItineraryItemsEnabled: false,
      }),
      [ANIMAL_ROW]
   );
});

test('Test_FilterVisibleScheduleModuleRows_TestItineraryFilterTalks_ExpectNeverShown', () => {
   const rows = [ANIMAL_ROW, GUARDIANS_TALK_ROW, WILD_ENCOUNTER_ROW];

   assert.deepEqual(
      ScheduleItemModuleSelection.filterVisibleScheduleModuleRows({
         rows,
         itinerary: {
            animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
            guardiansTalks: [{ name: 'Amur Tiger', start_time: '1:30 PM' }],
            wildEncounters: [{ name: 'African Rainforest', start_time: '2:00 PM' }],
         },
         onlyItineraryItemsEnabled: true,
      }),
      [ANIMAL_ROW]
   );
});

test('Test_ShouldClearSelectedScheduleRow_TestFilteredOut_ExpectCleared', () => {
   assert.equal(
      ScheduleItemModuleSelection.shouldClearSelectedScheduleRow({
         selectedRowId: 'Tiger||Savanna',
         visibleRows: [ATTRACTION_ROW],
      }),
      true
   );
   assert.equal(
      ScheduleItemModuleSelection.shouldClearSelectedScheduleRow({
         selectedRowId: 'Tiger||Savanna',
         visibleRows: [ANIMAL_ROW],
      }),
      false
   );
});

test('Test_ResolveScheduleModuleSearchLabel_TestKinds_ExpectTitles', () => {
   assert.equal(ScheduleItemModuleSelection.resolveScheduleModuleSearchLabel(ANIMAL_ROW), 'Tiger');
   assert.equal(ScheduleItemModuleSelection.resolveScheduleModuleSearchLabel(ATTRACTION_ROW), 'Carousel');
   assert.equal(
      ScheduleItemModuleSelection.resolveScheduleModuleSearchLabel(ZOOMOBILE_AS_ATTRACTION_ROW),
      'Zoomobile'
   );
   assert.equal(
      ScheduleItemModuleSelection.resolveScheduleModuleSearchLabel(TRANSPORTATION_ROW),
      'Zoomobile'
   );
});
