import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemModuleStore } from '../../../../../scripts/itinerary/panel/components/scheduleItemModuleStore.js';
import { ScheduleItemSearcher } from '../../../../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { AnimalSelectorModel } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { GuardiansTalkSelectorModel } from '../../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { WildEncounterSelectorModel } from '../../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';

const _EVENT_TYPES = ['lunch', 'break'];

const _ANIMAL_ROW = {
   species: 'Amur Tiger',
   exhibit: 'Savanna',
   scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
};

const _ATTRACTION_ROW = {
   name: 'Conservation Carousel',
   scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
};

const _GUARDIANS_TALK_ROW = {
   name: 'Amur Tiger',
   start_time: '1:30 PM',
   scheduleItemKind: ScheduleItemKind.GUARDIANS_TALK.itemType,
};

const _WILD_ENCOUNTER_ROW = {
   name: 'African Rainforest',
   start_time: '2:00 PM',
   scheduleItemKind: ScheduleItemKind.WILD_ENCOUNTER.itemType,
};

const _TRANSPORTATION_ROW = {
   name: 'Zoomobile',
   added_as_attraction: false,
   scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
};

const _ZOOMOBILE_AS_ATTRACTION_ROW = {
   name: 'Zoomobile',
   added_as_attraction: true,
   scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
};


test('Test_CanScheduleModuleSelection_TestMissingRow_ExpectFalse', () => {
   const canSchedule = ScheduleItemModuleStore.canScheduleModuleSelection({
      selection: ScheduleItemKind.ANIMAL.itemType,
      selectedRow: null,
      eventTypes: _EVENT_TYPES,
   });

   assert.equal(canSchedule, false);
});


test('Test_CanScheduleModuleSelection_TestAnimalRow_ExpectTrue', () => {
   const canSchedule = ScheduleItemModuleStore.canScheduleModuleSelection({
      selection: ScheduleItemKind.ANIMAL.itemType,
      selectedRow: _ANIMAL_ROW,
      eventTypes: _EVENT_TYPES,
   });

   assert.equal(canSchedule, true);
});


test('Test_CanScheduleModuleSelection_TestZoomobileAttraction_ExpectTrue', () => {
   const canSchedule = ScheduleItemModuleStore.canScheduleModuleSelection({
      selection: ScheduleItemKind.ATTRACTION.itemType,
      selectedRow: _ZOOMOBILE_AS_ATTRACTION_ROW,
      eventTypes: _EVENT_TYPES,
   });

   assert.equal(canSchedule, true);
});


test('Test_CanScheduleModuleSelection_TestTransportation_ExpectTrue', () => {
   const canSchedule = ScheduleItemModuleStore.canScheduleModuleSelection({
      selection: ScheduleItemKind.TRANSPORTATION.itemType,
      selectedRow: _TRANSPORTATION_ROW,
      eventTypes: _EVENT_TYPES,
   });

   assert.equal(canSchedule, true);
});


test('Test_CanScheduleModuleSelection_TestEventType_ExpectTrue', () => {
   const selection = _EVENT_TYPES.at(Position.FIRST);

   const canSchedule = ScheduleItemModuleStore.canScheduleModuleSelection({
      selection,
      selectedRow: null,
      eventTypes: _EVENT_TYPES,
   });

   assert.equal(canSchedule, true);
});


test('Test_CanScheduleModuleSelection_TestEmptySelection_ExpectFalse', () => {
   const canSchedule = ScheduleItemModuleStore.canScheduleModuleSelection({
      selection: '',
      selectedRow: null,
      eventTypes: _EVENT_TYPES,
   });

   assert.equal(canSchedule, false);
});


test('Test_FilterVisibleScheduleModuleRows_TestItineraryFilter_ExpectKeepsItineraryRows', () => {
   const rows = [_ANIMAL_ROW, _ATTRACTION_ROW];

   const visible = ScheduleItemModuleStore.filterVisibleScheduleModuleRows({
      rows,
      itinerary: {
         animals: [{ species: _ANIMAL_ROW.species, exhibit: _ANIMAL_ROW.exhibit }],
         attractions: [],
      },
      onlyItineraryItemsEnabled: true,
   });

   assert.deepEqual(visible, [_ANIMAL_ROW]);
});


test('Test_FilterVisibleScheduleModuleRows_TestFilterOff_ExpectAllRows', () => {
   const rows = [_ANIMAL_ROW, _ATTRACTION_ROW];

   const visible = ScheduleItemModuleStore.filterVisibleScheduleModuleRows({
      rows,
      onlyItineraryItemsEnabled: false,
   });

   assert.deepEqual(visible, rows);
});


test('Test_FilterVisibleScheduleModuleRows_TestScheduledTalks_ExpectHidden', () => {
   const rows = [_ANIMAL_ROW, _GUARDIANS_TALK_ROW, _WILD_ENCOUNTER_ROW];
   const itinerary = {
      animals: [],
      guardiansTalks: [{
         name: _GUARDIANS_TALK_ROW.name,
         start_time: _GUARDIANS_TALK_ROW.start_time,
      }],
      wildEncounters: [{
         name: _WILD_ENCOUNTER_ROW.name,
         start_time: _WILD_ENCOUNTER_ROW.start_time,
      }],
   };

   const visible = ScheduleItemModuleStore.filterVisibleScheduleModuleRows({
      rows,
      itinerary,
      onlyItineraryItemsEnabled: false,
   });

   assert.deepEqual(visible, [_ANIMAL_ROW]);
});


test('Test_FilterVisibleScheduleModuleRows_TestItineraryFilterTalks_ExpectNeverShown', () => {
   const rows = [_ANIMAL_ROW, _GUARDIANS_TALK_ROW, _WILD_ENCOUNTER_ROW];

   const visible = ScheduleItemModuleStore.filterVisibleScheduleModuleRows({
      rows,
      itinerary: {
         animals: [{ species: _ANIMAL_ROW.species, exhibit: _ANIMAL_ROW.exhibit }],
         guardiansTalks: [{
            name: _GUARDIANS_TALK_ROW.name,
            start_time: _GUARDIANS_TALK_ROW.start_time,
         }],
         wildEncounters: [{
            name: _WILD_ENCOUNTER_ROW.name,
            start_time: _WILD_ENCOUNTER_ROW.start_time,
         }],
      },
      onlyItineraryItemsEnabled: true,
   });

   assert.deepEqual(visible, [_ANIMAL_ROW]);
});


test('Test_ShouldClearSelectedScheduleRow_TestFilteredOut_ExpectCleared', () => {
   const selectedRowId = ScheduleItemSearcher.getScheduleItemRowId(_ANIMAL_ROW);

   const shouldClear = ScheduleItemModuleStore.shouldClearSelectedScheduleRow({
      selectedRowId,
      visibleRows: [_ATTRACTION_ROW],
   });

   assert.equal(shouldClear, true);
});


test('Test_ShouldClearSelectedScheduleRow_TestVisible_ExpectKept', () => {
   const selectedRowId = ScheduleItemSearcher.getScheduleItemRowId(_ANIMAL_ROW);

   const shouldClear = ScheduleItemModuleStore.shouldClearSelectedScheduleRow({
      selectedRowId,
      visibleRows: [_ANIMAL_ROW],
   });

   assert.equal(shouldClear, false);
});


test('Test_ShouldClearSelectedScheduleRow_TestMissingId_ExpectFalse', () => {
   const shouldClear = ScheduleItemModuleStore.shouldClearSelectedScheduleRow({
      selectedRowId: '',
      visibleRows: [_ANIMAL_ROW],
   });

   assert.equal(shouldClear, false);
});


test('Test_ResolveScheduleModuleSearchLabel_TestAnimal_ExpectSpecies', () => {
   const label = ScheduleItemModuleStore.resolveScheduleModuleSearchLabel(_ANIMAL_ROW);

   assert.equal(label, AnimalSelectorModel.getAnimalTitleLine(_ANIMAL_ROW));
});


test('Test_ResolveScheduleModuleSearchLabel_TestAttraction_ExpectName', () => {
   const label = ScheduleItemModuleStore.resolveScheduleModuleSearchLabel(_ATTRACTION_ROW);

   assert.equal(label, AttractionSelectorModel.getAttractionTitle(_ATTRACTION_ROW));
});


test('Test_ResolveScheduleModuleSearchLabel_TestZoomobileAttraction_ExpectName', () => {
   const label = ScheduleItemModuleStore.resolveScheduleModuleSearchLabel(
      _ZOOMOBILE_AS_ATTRACTION_ROW
   );

   assert.equal(label, AttractionSelectorModel.getAttractionTitle(_ZOOMOBILE_AS_ATTRACTION_ROW));
});


test('Test_ResolveScheduleModuleSearchLabel_TestTransportation_ExpectName', () => {
   const label = ScheduleItemModuleStore.resolveScheduleModuleSearchLabel(_TRANSPORTATION_ROW);

   assert.equal(label, TransportationSelectorModel.getTransportationName(_TRANSPORTATION_ROW));
});


test('Test_ResolveScheduleModuleSearchLabel_TestGuardiansTalk_ExpectName', () => {
   const label = ScheduleItemModuleStore.resolveScheduleModuleSearchLabel(_GUARDIANS_TALK_ROW);

   assert.equal(label, GuardiansTalkSelectorModel.getGuardiansTalkName(_GUARDIANS_TALK_ROW));
});


test('Test_ResolveScheduleModuleSearchLabel_TestWildEncounter_ExpectName', () => {
   const label = ScheduleItemModuleStore.resolveScheduleModuleSearchLabel(_WILD_ENCOUNTER_ROW);

   assert.equal(label, WildEncounterSelectorModel.getWildEncounterName(_WILD_ENCOUNTER_ROW));
});


test('Test_ResolveScheduleModuleSearchRowRenderer_TestKinds_ExpectDelegates', () => {
   const attractionResult = 'attraction';
   const transportationResult = 'transportation';
   const talkResult = 'talk';
   const wildResult = 'wild';
   const animalResult = 'animal';
   const calls = [];
   const renderers = {
      renderAnimalRowLeft: (row) => { calls.push(['animal', row]); return animalResult; },
      renderAttractionRowLeft: (row) => { calls.push(['attraction', row]); return attractionResult; },
      renderTransportationRowLeft: (row) => { calls.push(['transportation', row]); return transportationResult; },
      renderGuardiansTalkRowLeft: (row) => { calls.push(['talk', row]); return talkResult; },
      renderWildEncounterRowLeft: (row) => { calls.push(['wild', row]); return wildResult; },
   };

   const attraction = ScheduleItemModuleStore.resolveScheduleModuleSearchRowRenderer({
      row: _ATTRACTION_ROW,
      ...renderers,
   });
   const transportation = ScheduleItemModuleStore.resolveScheduleModuleSearchRowRenderer({
      row: _TRANSPORTATION_ROW,
      ...renderers,
   });
   const talk = ScheduleItemModuleStore.resolveScheduleModuleSearchRowRenderer({
      row: _GUARDIANS_TALK_ROW,
      ...renderers,
   });
   const wild = ScheduleItemModuleStore.resolveScheduleModuleSearchRowRenderer({
      row: _WILD_ENCOUNTER_ROW,
      ...renderers,
   });
   const animal = ScheduleItemModuleStore.resolveScheduleModuleSearchRowRenderer({
      row: _ANIMAL_ROW,
      ...renderers,
   });

   assert.equal(attraction, attractionResult);
   assert.equal(transportation, transportationResult);
   assert.equal(talk, talkResult);
   assert.equal(wild, wildResult);
   assert.equal(animal, animalResult);
   assert.deepEqual(calls.map(([kind]) => kind), [
      'attraction',
      'transportation',
      'talk',
      'wild',
      'animal',
   ]);
});
