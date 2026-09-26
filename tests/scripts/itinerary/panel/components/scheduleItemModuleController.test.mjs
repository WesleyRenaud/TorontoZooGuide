import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { ScheduleItemModuleController } from '../../../../../scripts/itinerary/panel/components/scheduleItemModuleController.js';
import { ItineraryConfirmationResult } from '../../../../../scripts/itinerary/itineraryConfirmationResult.js';
import { ScheduleItemSearcher } from '../../../../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { AnimalSelectorModel } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { TransportationSelectorModel } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { Strings } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';

const _EVENT_TYPES = ['lunch', 'break'];
const _STRINGS = {
   emptyResults: 'No results',
};

const _ANIMAL_ROW = {
   species: 'Amur Tiger',
   exhibit: 'Savanna',
   scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
};

function _createRefs({
   selection = '',
   searchValue = '',
   onlyItineraryItems = false,
} = {}) {
   const typeSelect = createDomNode('select', 'schedule-item-select');
   typeSelect.value = selection;

   const typeLabelEl = createDomNode('label', 'schedule-item-field-label');
   const searchInput = createDomNode('input', 'schedule-item-search-input');
   searchInput.value = searchValue;

   const resultsEl = createDomNode('div', 'schedule-item-results');
   const searchLabelEl = createDomNode('label', 'schedule-item-field-label');
   const onlyItineraryItemsWrap = createDomNode('div', 'schedule-item-only-itinerary-wrap');
   const onlyItineraryItemsCheckbox = createDomNode('input', 'schedule-item-only-itinerary-checkbox');
   onlyItineraryItemsCheckbox.checked = onlyItineraryItems;

   const scheduleButton = createDomNode('button', 'itin-finish');

   return {
      typeSelect,
      typeLabelEl,
      searchInput,
      resultsEl,
      searchLabelEl,
      onlyItineraryItemsWrap,
      onlyItineraryItemsCheckbox,
      scheduleButton,
   };
}

function _createController({
   refs,
   deps = {},
   scheduleTimeFields = {},
   ...options
} = {}) {
   return ScheduleItemModuleController.createScheduleItemModuleController({
      eventTypes: _EVENT_TYPES,
      strings: _STRINGS,
      itinerary: {
         animals: [{ species: _ANIMAL_ROW.species, exhibit: _ANIMAL_ROW.exhibit }],
         attractions: [],
      },
      scheduleTimeFields,
      renderAnimalRowLeft: () => createDomNode('span', 'animal-row'),
      renderAttractionRowLeft: () => createDomNode('span', 'attraction-row'),
      refs,
      scheduleButton: refs.scheduleButton,
      deps,
      ...options,
   });
}

let searchRequests = [];

beforeEach(() => {
   searchRequests = [];
});

afterEach(() => {
   searchRequests = [];
});


test('Test_UpdateFieldVisibility_TestEventType_ExpectSearchDisabled', () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   const controller = _createController({ refs });

   controller.updateFieldVisibility();

   assert.equal(refs.searchInput.disabled, true);
   assert.equal(refs.searchInput.getAttribute('aria-disabled'), 'true');
   assert.equal(refs.onlyItineraryItemsWrap.hidden, true);
   assert.equal(refs.scheduleButton.disabled, false);
});


test('Test_UpdateFieldVisibility_TestAnimalWithoutRow_ExpectScheduleDisabled', () => {
   const refs = _createRefs({ selection: ScheduleItemKind.ANIMAL.itemType });
   const controller = _createController({ refs });

   controller.updateFieldVisibility();

   assert.equal(refs.typeSelect.disabled, false);
   assert.equal(refs.searchInput.disabled, false);
   assert.equal(refs.onlyItineraryItemsCheckbox.disabled, false);
   assert.equal(refs.scheduleButton.disabled, true);
});


test('Test_Initialize_TestPreselectedRow_ExpectLockedFields', () => {
   const refs = _createRefs();
   const controller = _createController({
      refs,
      preselectedRow: _ANIMAL_ROW,
      deps: {
         renderSearchResults: () => {},
      },
   });

   controller.initialize();

   assert.equal(refs.typeSelect.disabled, true);
   assert.equal(refs.typeSelect.getAttribute('aria-disabled'), 'true');
   assert.equal(refs.typeLabelEl.classList.contains('is-disabled'), true);
   assert.equal(refs.searchInput.disabled, true);
   assert.equal(refs.searchInput.getAttribute('aria-disabled'), 'true');
   assert.equal(refs.searchLabelEl.classList.contains('is-disabled'), true);
   assert.equal(refs.onlyItineraryItemsCheckbox.disabled, true);
   assert.equal(refs.onlyItineraryItemsWrap.hidden, false);
   assert.equal(refs.scheduleButton.disabled, false);
});


test('Test_DisplaySearchResults_TestItineraryFilter_ExpectKeepsItineraryRows', () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      onlyItineraryItems: true,
   });
   const renderedRows = [];
   const controller = _createController({
      refs,
      deps: {
         renderSearchResults: ({ rows }) => {
            renderedRows.push(rows);
         },
      },
   });

   controller.displaySearchResults([
      _ANIMAL_ROW,
      {
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
      },
   ]);

   assert.deepEqual(renderedRows, [[_ANIMAL_ROW]]);
});


test('Test_RunSearch_TestStaleResponses_ExpectIgnored', async () => {
   const query = 'tiger';
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: query,
   });
   const controller = _createController({
      refs,
      deps: {
         getSearchContext: async () => ({ temp: null }),
         searchItineraryItems: async (_url, payload) => {
            searchRequests.push(payload);

            if (searchRequests.length === 1) {
               await new Promise((resolve) => {
                  setTimeout(resolve, 20);
               });
               return {
                  animals: [{
                     species: 'Stale',
                     exhibit: 'Old',
                     scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
                  }],
               };
            }

            return { animals: [_ANIMAL_ROW] };
         },
         renderSearchResults: ({ rows }) => {
            refs.resultsEl.latestRows = rows;
         },
      },
   });

   const firstSearch = controller.runSearch();
   const secondSearch = controller.runSearch();
   await Promise.all([firstSearch, secondSearch]);

   assert.deepEqual(searchRequests, [
      {
         query,
         includeAnimals: true,
         includeOffDisplayAnimals: true,
         forItinerary: true,
         temp: null,
      },
      {
         query,
         includeAnimals: true,
         includeOffDisplayAnimals: true,
         forItinerary: true,
         temp: null,
      },
   ]);
   assert.deepEqual(refs.resultsEl.latestRows, [_ANIMAL_ROW]);
});


test('Test_HandleSchedule_TestDurationOnly_ExpectScheduled', async () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   const scheduleOptions = {
      startTime: '',
      durationMinutes: TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
   };
   const scheduledOptions = [];
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         getScheduleTimeOptions: () => scheduleOptions,
      },
      deps: {
         scheduleSelectedItem: async (
            _itinerary,
            _selection,
            _selectedRow,
            _eventTypes,
            options
         ) => {
            scheduledOptions.push(options);
            return { errorType: 'success' };
         },
         itinerarySuccess: (errorType) => errorType === 'success',
      },
   });

   await controller.handleSchedule();

   assert.deepEqual(scheduledOptions, [scheduleOptions]);
});


test('Test_HandleSchedule_TestSuccess_ExpectDismissed', async () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   let dismissed = false;
   let scheduled = false;
   const controller = _createController({
      refs,
      onScheduled: async () => {
         scheduled = true;
      },
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({
            startTime: '12:00 PM',
            durationMinutes: TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
         }),
      },
      deps: {
         scheduleSelectedItem: async () => ({ errorType: 'success' }),
         itinerarySuccess: (errorType) => errorType === 'success',
         requiresNotOnItineraryConfirmation: () => false,
      },
   });

   await controller.handleSchedule({
      dismissPopup: () => {
         dismissed = true;
      },
   });

   assert.equal(dismissed, true);
   assert.equal(scheduled, true);
   assert.equal(refs.scheduleButton.disabled, false);
});


test('Test_ApplyPreselectedRow_TestAnimal_ExpectLockedSelection', () => {
   const refs = _createRefs();
   const controller = ScheduleItemModuleController.createScheduleItemModuleController({
      eventTypes: _EVENT_TYPES,
      strings: _STRINGS,
      preselectedRow: _ANIMAL_ROW,
      refs,
      scheduleButton: refs.scheduleButton,
      renderAnimalRowLeft: () => createDomNode('span', 'animal-row'),
      renderAttractionRowLeft: () => createDomNode('span', 'attraction-row'),
      deps: {
         renderSearchResults: () => {},
      },
   });

   controller.applyPreselectedRow();

   assert.equal(refs.typeSelect.value, ScheduleItemKind.ANIMAL.itemType);
   assert.equal(refs.searchInput.value, AnimalSelectorModel.getAnimalTitleLine(_ANIMAL_ROW));
   assert.equal(controller.canScheduleSelection(), true);
   assert.equal(refs.typeSelect.disabled, true);
   assert.equal(refs.searchInput.disabled, true);
   assert.equal(refs.onlyItineraryItemsCheckbox.disabled, true);
});


test('Test_ApplyPreselectedRow_TestZoomobileAttraction_ExpectAttractionType', () => {
   const refs = _createRefs();
   const rideName = 'Zoomobile';
   const durationMinutes = 75;
   const zoomobileRow = {
      name: rideName,
      added_as_attraction: true,
      route_duration_minutes: durationMinutes,
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
   };
   const controller = ScheduleItemModuleController.createScheduleItemModuleController({
      eventTypes: _EVENT_TYPES,
      strings: _STRINGS,
      itinerary: {
         attractions: [],
         transportations: [{
            name: rideName,
            added_as_attraction: true,
         }],
      },
      preselectedRow: zoomobileRow,
      refs,
      scheduleButton: refs.scheduleButton,
      renderAnimalRowLeft: () => createDomNode('span', 'animal-row'),
      renderAttractionRowLeft: () => createDomNode('span', 'attraction-row'),
      renderTransportationRowLeft: () => createDomNode('span', 'transportation-row'),
      deps: {
         renderSearchResults: ({ rows }) => {
            refs.resultsEl.latestRows = rows;
         },
      },
   });

   controller.applyPreselectedRow();

   assert.equal(refs.typeSelect.value, ScheduleItemKind.ATTRACTION.itemType);
   assert.equal(refs.searchInput.value, AttractionSelectorModel.getAttractionTitle(zoomobileRow));
   assert.deepEqual(refs.resultsEl.latestRows, [zoomobileRow]);
   assert.equal(controller.canScheduleSelection(), true);
   assert.equal(refs.scheduleButton.disabled, false);
});


test('Test_ApplyPreselectedRow_TestTransportation_ExpectTransportationType', () => {
   const refs = _createRefs();
   const rideName = 'Zoomobile';
   const zoomobileRow = {
      name: rideName,
      added_as_attraction: false,
      scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
   };
   const controller = ScheduleItemModuleController.createScheduleItemModuleController({
      eventTypes: _EVENT_TYPES,
      strings: _STRINGS,
      itinerary: {
         attractions: [],
         transportations: [{
            name: rideName,
            added_as_attraction: false,
         }],
      },
      preselectedRow: zoomobileRow,
      refs,
      scheduleButton: refs.scheduleButton,
      renderAnimalRowLeft: () => createDomNode('span', 'animal-row'),
      renderAttractionRowLeft: () => createDomNode('span', 'attraction-row'),
      renderTransportationRowLeft: () => createDomNode('span', 'transportation-row'),
      deps: {
         renderSearchResults: ({ rows }) => {
            refs.resultsEl.latestRows = rows;
         },
      },
   });

   controller.applyPreselectedRow();

   assert.equal(refs.typeSelect.value, ScheduleItemKind.TRANSPORTATION.itemType);
   assert.equal(
      refs.searchInput.value,
      TransportationSelectorModel.getTransportationName(zoomobileRow)
   );
   assert.deepEqual(refs.resultsEl.latestRows, [zoomobileRow]);
   assert.equal(controller.canScheduleSelection(), true);
});


test('Test_DisplaySearchResults_TestSelectRow_ExpectInferredType', () => {
   const refs = _createRefs({ selection: '' });
   let onSelectRow = null;
   const controller = _createController({
      refs,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow, selectedRowId }) => {
            onSelectRow = selectRow;
            refs.resultsEl.selectedRowId = selectedRowId;
         },
      },
   });
   const rowId = ScheduleItemSearcher.getScheduleItemRowId(_ANIMAL_ROW);

   controller.displaySearchResults([_ANIMAL_ROW]);
   onSelectRow?.(_ANIMAL_ROW, rowId);

   assert.equal(refs.typeSelect.value, ScheduleItemKind.ANIMAL.itemType);
   assert.equal(refs.resultsEl.selectedRowId, rowId);
   assert.equal(controller.canScheduleSelection(), true);
   assert.equal(refs.scheduleButton.disabled, false);
});


test('Test_DisplaySearchResults_TestSameRowAgain_ExpectCleared', () => {
   const refs = _createRefs({ selection: ScheduleItemKind.ANIMAL.itemType });
   let onSelectRow = null;
   const controller = _createController({
      refs,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });
   const rowId = ScheduleItemSearcher.getScheduleItemRowId(_ANIMAL_ROW);

   controller.displaySearchResults([_ANIMAL_ROW]);
   onSelectRow?.(_ANIMAL_ROW, rowId);
   onSelectRow?.(_ANIMAL_ROW, rowId);

   assert.equal(controller.canScheduleSelection(), false);
   assert.equal(refs.scheduleButton.disabled, true);
});


test('Test_UpdateFieldVisibility_TestSelectedTalk_ExpectLockedTimes', () => {
   const refs = _createRefs({ selection: ScheduleItemKind.GUARDIANS_TALK.itemType });
   let fixedTimeMode = null;
   let onSelectRow = null;
   const talkRow = {
      name: 'Amur Tiger',
      start_time: '10:30',
      maximum_duration: TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
      scheduleItemKind: ScheduleItemKind.GUARDIANS_TALK.itemType,
   };
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         setFixedTimeScheduleMode: (options) => {
            fixedTimeMode = options;
         },
         setFixedDurationScheduleMode: () => {},
         reset: () => {
            fixedTimeMode = { lockTimes: false };
         },
      },
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });

   controller.displaySearchResults([talkRow]);
   onSelectRow?.(talkRow, talkRow.name);

   assert.deepEqual(fixedTimeMode, { lockTimes: true });
});


test('Test_HandleTypeSelectChange_TestAfterTalk_ExpectTimesUnlocked', () => {
   const refs = _createRefs({ selection: ScheduleItemKind.GUARDIANS_TALK.itemType });
   let fixedTimeMode = null;
   let onSelectRow = null;
   const talkRow = {
      name: 'Amur Tiger',
      start_time: '10:30',
      maximum_duration: TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
      scheduleItemKind: ScheduleItemKind.GUARDIANS_TALK.itemType,
   };
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         setFixedTimeScheduleMode: (options) => {
            fixedTimeMode = options;
         },
         setFixedDurationScheduleMode: () => {},
         reset: () => {
            fixedTimeMode = { lockTimes: false };
         },
      },
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });

   controller.displaySearchResults([talkRow]);
   onSelectRow?.(talkRow, talkRow.name);
   controller.handleTypeSelectChange();

   assert.deepEqual(fixedTimeMode, { lockTimes: false });
});


test('Test_UpdateFieldVisibility_TestTransportation_ExpectLockedDuration', () => {
   const refs = _createRefs({ selection: ScheduleItemKind.TRANSPORTATION.itemType });
   const durationMinutes = 75;
   let fixedDurationMode = null;
   let onSelectRow = null;
   const zoomobileRow = {
      name: 'Zoomobile',
      route_duration_minutes: durationMinutes,
      scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
   };
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         setFixedTimeScheduleMode: () => {},
         setFixedDurationScheduleMode: (options) => {
            fixedDurationMode = options;
         },
         reset: () => {
            fixedDurationMode = { lockDuration: false };
         },
      },
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });

   controller.displaySearchResults([zoomobileRow]);
   onSelectRow?.(zoomobileRow, zoomobileRow.name);

   assert.deepEqual(fixedDurationMode, {
      lockDuration: true,
      durationMinutes,
   });
});


test('Test_UpdateFieldVisibility_TestZoomobileAttraction_ExpectLockedDuration', () => {
   const refs = _createRefs({ selection: ScheduleItemKind.ATTRACTION.itemType });
   const durationMinutes = 75;
   let fixedDurationMode = null;
   let onSelectRow = null;
   const zoomobileRow = {
      name: 'Zoomobile',
      added_as_attraction: true,
      route_duration_minutes: durationMinutes,
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
   };
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         setFixedTimeScheduleMode: () => {},
         setFixedDurationScheduleMode: (options) => {
            fixedDurationMode = options;
         },
         reset: () => {
            fixedDurationMode = { lockDuration: false };
         },
      },
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });

   controller.displaySearchResults([zoomobileRow]);
   onSelectRow?.(zoomobileRow, zoomobileRow.name);

   assert.deepEqual(fixedDurationMode, {
      lockDuration: true,
      durationMinutes,
   });
});


test('Test_HandleTypeSelectChange_TestClearsSearch_ExpectReset', () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   let resetCount = 0;
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         reset: () => {
            resetCount += 1;
         },
      },
   });

   controller.handleTypeSelectChange();

   assert.equal(refs.searchInput.value, '');
   assert.equal(resetCount, 1);
   assert.equal(controller.canScheduleSelection(), false);
});


test('Test_HandleOnlyItineraryItemsChange_TestCachedRows_ExpectFiltered', () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
   });
   const renderedRows = [];
   const controller = _createController({
      refs,
      deps: {
         renderSearchResults: ({ rows }) => {
            renderedRows.push(rows);
         },
      },
   });

   controller.displaySearchResults([
      _ANIMAL_ROW,
      {
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
      },
   ]);
   refs.onlyItineraryItemsCheckbox.checked = true;
   controller.handleOnlyItineraryItemsChange();

   assert.deepEqual(renderedRows.at(Position.LAST), [_ANIMAL_ROW]);
});


test('Test_DisplaySearchResults_TestSearchDisabled_ExpectCleared', () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   refs.resultsEl.appendChild(createDomNode('div', 'existing-result'));
   const controller = _createController({ refs });

   controller.displaySearchResults([_ANIMAL_ROW]);

   assert.equal(refs.resultsEl.children.length, 0);
});


test('Test_RunSearch_TestSearchDisabled_ExpectCleared', async () => {
   const refs = _createRefs({
      selection: _EVENT_TYPES.at(Position.FIRST),
      searchValue: 'tiger',
   });
   refs.resultsEl.appendChild(createDomNode('div', 'existing-result'));
   const controller = _createController({ refs });

   await controller.runSearch();

   assert.equal(refs.resultsEl.children.length, 0);
});


test('Test_RunSearch_TestEmptyQuery_ExpectCleared', async () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: '',
   });
   refs.resultsEl.appendChild(createDomNode('div', 'existing-result'));
   const controller = _createController({ refs });

   await controller.runSearch();

   assert.equal(refs.resultsEl.children.length, 0);
});


test('Test_RunSearch_TestFailure_ExpectEmptyRows', async () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   const renderedRows = [];
   const controller = _createController({
      refs,
      deps: {
         getSearchContext: async () => ({}),
         searchItineraryItems: async () => {
            throw new Error('search failed');
         },
         renderSearchResults: ({ rows }) => {
            renderedRows.push(rows);
         },
      },
   });

   await controller.runSearch();

   assert.deepEqual(renderedRows, [[]]);
});


test('Test_HandleSchedule_TestValidationError_ExpectNotice', async () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   const errorMessage = 'Validation failed';
   const notices = [];
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({}),
      },
      deps: {
         scheduleSelectedItem: async () => ({ errorType: 'validationError' }),
         itinerarySuccess: () => false,
         requiresNotOnItineraryConfirmation: () => false,
         resolveErrorMessage: () => errorMessage,
         showNotice: (message) => {
            notices.push(message);
         },
      },
   });

   await controller.handleSchedule();

   assert.deepEqual(notices, [errorMessage]);
});


test('Test_HandleSchedule_TestThrownError_ExpectGenericNotice', async () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   const notices = [];
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({}),
      },
      deps: {
         scheduleSelectedItem: async () => {
            throw new Error('network');
         },
         showNotice: (message) => {
            notices.push(message);
         },
      },
   });

   await controller.handleSchedule();

   assert.equal(notices.at(Position.LAST), Strings.itinerary.errors.generic);
});


test('Test_HandleSchedule_TestNotOnItinerary_ExpectSilent', async () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   const notices = [];
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({}),
      },
      deps: {
         scheduleSelectedItem: async () => ({ errorType: 'notOnItinerary' }),
         itinerarySuccess: () => false,
         requiresNotOnItineraryConfirmation: () => true,
         showNotice: (message) => {
            notices.push(message);
         },
      },
   });

   await controller.handleSchedule();

   assert.deepEqual(notices, []);
});


test('Test_HandleSchedule_TestDuplicateSubmission_ExpectSingleCall', async () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   let scheduleCalls = 0;
   let resolveSchedule = null;
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({}),
      },
      deps: {
         scheduleSelectedItem: async () => {
            scheduleCalls += 1;
            await new Promise((resolve) => {
               resolveSchedule = resolve;
            });
            return { errorType: 'success' };
         },
         itinerarySuccess: (errorType) => errorType === 'success',
         requiresNotOnItineraryConfirmation: () => false,
      },
   });

   const firstSchedule = controller.handleSchedule();
   const secondSchedule = controller.handleSchedule();
   resolveSchedule?.();
   await Promise.all([firstSchedule, secondSchedule]);

   assert.equal(scheduleCalls, 1);
});


test('Test_Initialize_TestPreselectedResultClick_ExpectKept', () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: AnimalSelectorModel.getAnimalTitleLine(_ANIMAL_ROW),
   });
   let onSelectRow = null;
   const controller = _createController({
      refs,
      preselectedRow: _ANIMAL_ROW,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });
   const rowId = ScheduleItemSearcher.getScheduleItemRowId(_ANIMAL_ROW);

   controller.initialize();
   onSelectRow?.(_ANIMAL_ROW, rowId);

   assert.equal(controller.canScheduleSelection(), true);
});


test('Test_HandleSearchInput_TestClearsSelection_ExpectSearchTriggered', () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   const searchCalls = [];
   let onSelectRow = null;
   const controller = _createController({
      refs,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });
   const rowId = ScheduleItemSearcher.getScheduleItemRowId(_ANIMAL_ROW);

   controller.displaySearchResults([_ANIMAL_ROW]);
   onSelectRow?.(_ANIMAL_ROW, rowId);
   controller.handleSearchInput(() => {
      searchCalls.push('search');
   });

   assert.equal(controller.canScheduleSelection(), false);
   assert.deepEqual(searchCalls, ['search']);
});


test('Test_HandleOnlyItineraryItemsChange_TestNoCachedRows_ExpectSearch', async () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   const requests = [];
   const controller = _createController({
      refs,
      deps: {
         getSearchContext: async () => ({}),
         searchItineraryItems: async (_url, payload) => {
            requests.push(payload);
            return { animals: [_ANIMAL_ROW] };
         },
         renderSearchResults: () => {},
      },
   });

   refs.onlyItineraryItemsCheckbox.checked = true;
   await controller.handleOnlyItineraryItemsChange();

   assert.equal(requests.length, 1);
});


test('Test_Initialize_TestWithoutPreselected_ExpectClearedResults', () => {
   const refs = _createRefs({ selection: ScheduleItemKind.ANIMAL.itemType });
   refs.resultsEl.appendChild(createDomNode('div', 'existing-result'));
   const controller = _createController({ refs });

   controller.initialize();

   assert.equal(refs.resultsEl.children.length, 0);
   assert.equal(refs.scheduleButton.disabled, true);
});


test('Test_BindEvents_TestScheduleClick_ExpectDismissed', async () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   let dismissed = false;
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({}),
      },
      deps: {
         scheduleSelectedItem: async () => ({ errorType: 'success' }),
         itinerarySuccess: (errorType) => errorType === 'success',
         requiresNotOnItineraryConfirmation: () => false,
      },
   });

   controller.bindEvents({
      popup: {
         dismiss: () => {
            dismissed = true;
         },
      },
      scheduleSearch: () => {},
   });
   refs.scheduleButton.click();
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.equal(dismissed, true);
});


test('Test_BindEvents_TestTypeChange_ExpectClearsSearch', () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   const controller = _createController({
      refs,
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({}),
      },
      deps: {
         scheduleSelectedItem: async () => ({ errorType: 'success' }),
         itinerarySuccess: (errorType) => errorType === 'success',
         requiresNotOnItineraryConfirmation: () => false,
      },
   });

   controller.bindEvents({
      popup: { dismiss: () => {} },
      scheduleSearch: () => {},
   });
   refs.typeSelect.value = ScheduleItemKind.ANIMAL.itemType;
   refs.typeSelect.listeners.change?.();
   refs.searchInput.listeners.input?.();

   assert.equal(refs.searchInput.value, '');
});


test('Test_DisplaySearchResults_TestHiddenByFilter_ExpectCleared', () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
   });
   let onSelectRow = null;
   const panda = {
      species: 'Giant Panda',
      exhibit: 'Bamboo',
      scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
   };
   const controller = _createController({
      refs,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });

   controller.displaySearchResults([_ANIMAL_ROW, panda]);
   onSelectRow?.(panda, ScheduleItemSearcher.getScheduleItemRowId(panda));
   refs.onlyItineraryItemsCheckbox.checked = true;
   controller.handleOnlyItineraryItemsChange();

   assert.equal(controller.canScheduleSelection(), false);
});


test('Test_DisplaySearchResults_TestRenderRowLeft_ExpectModuleRenderer', () => {
   const refs = _createRefs({ selection: ScheduleItemKind.ANIMAL.itemType });
   const rendered = [];
   const controller = _createController({
      refs,
      renderAnimalRowLeft: () => createDomNode('span', 'animal-row'),
      deps: {
         renderSearchResults: ({ renderRowLeft, rows }) => {
            rendered.push(renderRowLeft(rows.at(Position.FIRST)));
         },
      },
   });

   controller.displaySearchResults([_ANIMAL_ROW]);

   assert.equal(rendered.length, 1);
   assert.ok(rendered.at(Position.FIRST));
});


test('Test_ApplyPreselectedRow_TestMissing_ExpectNoOp', () => {
   const refs = _createRefs();
   const controller = _createController({ refs });

   controller.applyPreselectedRow();

   assert.equal(controller.canScheduleSelection(), false);
});


test('Test_RunSearch_TestStaleFailure_ExpectIgnored', async () => {
   const refs = _createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   const renderedRows = [];
   let searchCalls = 0;
   const controller = _createController({
      refs,
      deps: {
         getSearchContext: async () => ({}),
         searchItineraryItems: async () => {
            searchCalls += 1;

            if (searchCalls === 1) {
               await new Promise((resolve) => {
                  setTimeout(resolve, 20);
               });
               throw new Error('stale failure');
            }

            return { animals: [_ANIMAL_ROW] };
         },
         renderSearchResults: ({ rows }) => {
            renderedRows.push(rows);
         },
      },
   });

   const firstSearch = controller.runSearch();
   const secondSearch = controller.runSearch();
   await Promise.all([firstSearch, secondSearch]);

   assert.deepEqual(renderedRows.at(Position.LAST), [_ANIMAL_ROW]);
   assert.equal(renderedRows.some((rows) => rows.length === 0), false);
});


test('Test_HandleSchedule_TestCancelledConfirmation_ExpectSilentReturn', async () => {
   const refs = _createRefs({ selection: _EVENT_TYPES.at(Position.FIRST) });
   const notices = [];
   const originalIsCancelled = ItineraryConfirmationResult.isItineraryConfirmationCancelled;

   ItineraryConfirmationResult.isItineraryConfirmationCancelled = () => true;

   try {
      const controller = _createController({
         refs,
         scheduleTimeFields: {
            getScheduleTimeOptions: () => ({}),
         },
         deps: {
            scheduleSelectedItem: async () => ({ cancelled: true }),
            itinerarySuccess: () => false,
            requiresNotOnItineraryConfirmation: () => false,
            showNotice: (message) => {
               notices.push(message);
            },
         },
      });
      await controller.handleSchedule({
         dismissPopup: () => {
            notices.push('dismissed');
         },
      });

      assert.deepEqual(notices, []);
   } finally {
      ItineraryConfirmationResult.isItineraryConfirmationCancelled = originalIsCancelled;
   }
});
