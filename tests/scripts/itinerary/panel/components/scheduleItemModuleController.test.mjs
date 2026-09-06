import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { ScheduleItemModuleController } from '../../../../../scripts/itinerary/panel/components/scheduleItemModuleController.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';

const EVENT_TYPES = ['lunch', 'break'];
const STRINGS = {
   emptyResults: 'No results',
};

const ANIMAL_ROW = {
   species: 'Tiger',
   exhibit: 'Savanna',
   scheduleItemKind: 'animals',
};

function createRefs({
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

function createController({
   refs,
   deps = {},
   scheduleTimeFields = {},
   ...options
} = {}) {
   return ScheduleItemModuleController.createScheduleItemModuleController({
      eventTypes: EVENT_TYPES,
      strings: STRINGS,
      itinerary: {
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
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

test('Test_UpdateFieldVisibility_TestUpdateFieldVisibilityDisablesSearchForEventTypeSelections_ExpectOk', () => {
   const refs = createRefs({ selection: 'lunch' });
   const controller = createController({ refs });

   controller.updateFieldVisibility();

   assert.equal(refs.searchInput.disabled, true);
   assert.equal(refs.searchInput.getAttribute('aria-disabled'), 'true');
   assert.equal(refs.onlyItineraryItemsWrap.hidden, true);
   assert.equal(refs.scheduleButton.disabled, false);
});

test('Test_UpdateFieldVisibility_TestUpdateFieldVisibilityKeepsTheScheduleButtonDisabledUntilA_ExpectOk', () => {
   const refs = createRefs({ selection: ScheduleItemKind.ANIMAL.itemType });
   const controller = createController({ refs });

   controller.updateFieldVisibility();

   assert.equal(refs.typeSelect.disabled, false);
   assert.equal(refs.searchInput.disabled, false);
   assert.equal(refs.onlyItineraryItemsCheckbox.disabled, false);
   assert.equal(refs.scheduleButton.disabled, true);
});

test('Test_Initialize_TestInitializeLocksTypeSearchAndItineraryFilterFor_ExpectOk', () => {
   const refs = createRefs();
   const controller = createController({
      refs,
      preselectedRow: ANIMAL_ROW,
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

test('Test_DisplaySearchResults_TestDisplaySearchResultsFiltersRowsToItineraryItemsWhenEnabled_ExpectOk', () => {
   const refs = createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      onlyItineraryItems: true,
   });
   const renderedRows = [];
   const controller = createController({
      refs,
      deps: {
         renderSearchResults: ({ rows }) => {
            renderedRows.push(rows);
         },
      },
   });

   controller.displaySearchResults([
      ANIMAL_ROW,
      {
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         scheduleItemKind: 'animals',
      },
   ]);

   assert.deepEqual(renderedRows, [[ANIMAL_ROW]]);
});

test('Test_RunSearch_TestRunSearchFetchesRowsAndIgnoresStaleResponses_ExpectOk', async () => {
   const refs = createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   const controller = createController({
      refs,
      deps: {
         getSearchContext: async () => ({ temp: null }),
         searchItineraryItems: async (_url, payload) => {
            searchRequests.push(payload);

            if (searchRequests.length === 1) {
               await new Promise((resolve) => {
                  setTimeout(resolve, 20);
               });
               return { animals: [{ species: 'Stale', exhibit: 'Old', scheduleItemKind: 'animals' }] };
            }

            return { animals: [ANIMAL_ROW] };
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
         query: 'tiger',
         includeAnimals: true,
         forItinerary: true,
         temp: null,
      },
      {
         query: 'tiger',
         includeAnimals: true,
         forItinerary: true,
         temp: null,
      },
   ]);
   assert.deepEqual(refs.resultsEl.latestRows, [ANIMAL_ROW]);
});

test('Test_HandleSchedule_TestHandleScheduleAllowsDurationWithoutAStartTime_ExpectOk', async () => {
   const refs = createRefs({ selection: 'lunch' });
   const scheduledOptions = [];
   const controller = createController({
      refs,
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({
            startTime: '',
            durationMinutes: 30,
         }),
      },
      deps: {
         scheduleSelectedItem: async (
            _itinerary,
            _selection,
            _selectedRow,
            _eventTypes,
            scheduleOptions
         ) => {
            scheduledOptions.push(scheduleOptions);
            return { errorType: 'success' };
         },
         itinerarySuccess: (errorType) => errorType === 'success',
      },
   });

   await controller.handleSchedule();

   assert.deepEqual(scheduledOptions, [{
      startTime: '',
      durationMinutes: 30,
   }]);
});

test('Test_HandleSchedule_TestHandleScheduleDismissesThePopupAfterASuccessfulSchedule_ExpectOk', async () => {
   const refs = createRefs({ selection: 'lunch' });
   let dismissed = false;
   let scheduled = false;
   const controller = createController({
      refs,
      onScheduled: async () => {
         scheduled = true;
      },
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({
            startTime: '12:00 PM',
            durationMinutes: 30,
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

test('Test_ApplyPreselectedRow_TestApplyPreselectedRowSeedsTheTypeSearchInputAndSelected_ExpectOk', () => {
   const refs = createRefs();
   const controller = ScheduleItemModuleController.createScheduleItemModuleController({
      eventTypes: EVENT_TYPES,
      strings: STRINGS,
      preselectedRow: ANIMAL_ROW,
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
   assert.equal(refs.searchInput.value, 'Tiger');
   assert.equal(controller.canScheduleSelection(), true);
   assert.equal(refs.typeSelect.disabled, true);
   assert.equal(refs.searchInput.disabled, true);
   assert.equal(refs.onlyItineraryItemsCheckbox.disabled, true);
});

test('Test_ApplyPreselectedRow_TestApplyPreselectedRowTreatsUnscheduledZoomobileAsAnAttraction_ExpectOk', () => {
   const refs = createRefs();
   const zoomobileRow = {
      name: 'Zoomobile',
      added_as_attraction: true,
      route_duration_minutes: 75,
      scheduleItemKind: 'attractions',
   };
   const controller = ScheduleItemModuleController.createScheduleItemModuleController({
      eventTypes: EVENT_TYPES,
      strings: STRINGS,
      itinerary: {
         attractions: [],
         transportations: [{
            name: 'Zoomobile',
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
   assert.equal(refs.searchInput.value, 'Zoomobile');
   assert.deepEqual(refs.resultsEl.latestRows, [zoomobileRow]);
   assert.equal(controller.canScheduleSelection(), true);
   assert.equal(refs.scheduleButton.disabled, false);
});

test('Test_ApplyPreselectedRow_TestApplyPreselectedRowKeepsTransportationThatWasNotAddedAs_ExpectOk', () => {
   const refs = createRefs();
   const zoomobileRow = {
      name: 'Zoomobile',
      added_as_attraction: false,
      scheduleItemKind: 'transportations',
   };
   const controller = ScheduleItemModuleController.createScheduleItemModuleController({
      eventTypes: EVENT_TYPES,
      strings: STRINGS,
      itinerary: {
         attractions: [],
         transportations: [{
            name: 'Zoomobile',
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
   assert.equal(refs.searchInput.value, 'Zoomobile');
   assert.deepEqual(refs.resultsEl.latestRows, [zoomobileRow]);
   assert.equal(controller.canScheduleSelection(), true);
});

test('Test_DisplaySearchResults_TestDisplaySearchResultsSelectsARowAndInfersTheModule_ExpectOk', () => {
   const refs = createRefs({ selection: '' });
   let onSelectRow = null;
   const controller = createController({
      refs,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow, selectedRowId }) => {
            onSelectRow = selectRow;
            refs.resultsEl.selectedRowId = selectedRowId;
         },
      },
   });

   controller.displaySearchResults([ANIMAL_ROW]);
   onSelectRow?.(ANIMAL_ROW, 'Tiger||Savanna');

   assert.equal(refs.typeSelect.value, ScheduleItemKind.ANIMAL.itemType);
   assert.equal(refs.resultsEl.selectedRowId, 'Tiger||Savanna');
   assert.equal(controller.canScheduleSelection(), true);
   assert.equal(refs.scheduleButton.disabled, false);
});

test('Test_DisplaySearchResults_TestDisplaySearchResultsClearsTheSelectionWhenTheSameRow_ExpectOk', () => {
   const refs = createRefs({ selection: ScheduleItemKind.ANIMAL.itemType });
   let onSelectRow = null;
   const controller = createController({
      refs,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });

   controller.displaySearchResults([ANIMAL_ROW]);
   onSelectRow?.(ANIMAL_ROW, 'Tiger||Savanna');
   onSelectRow?.(ANIMAL_ROW, 'Tiger||Savanna');

   assert.equal(controller.canScheduleSelection(), false);
   assert.equal(refs.scheduleButton.disabled, true);
});

test('Test_UpdateFieldVisibility_TestUpdateFieldVisibilityDisablesTimeFieldsForSelectedTalksAnd_ExpectOk', () => {
   const refs = createRefs({ selection: ScheduleItemKind.GUARDIANS_TALK.itemType });
   let fixedTimeMode = null;
   let onSelectRow = null;
   const talkRow = {
      name: 'Amur Tiger',
      start_time: '10:30',
      maximum_duration: 30,
      scheduleItemKind: 'guardians_talks',
   };
   const controller = createController({
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
   onSelectRow?.(talkRow, 'Amur Tiger');

   assert.deepEqual(fixedTimeMode, { lockTimes: true });

   controller.handleTypeSelectChange();

   assert.deepEqual(fixedTimeMode, { lockTimes: false });
});

test('Test_UpdateFieldVisibility_TestUpdateFieldVisibilityLocksTransportationDurationToTheRouteTotal_ExpectOk', () => {
   const refs = createRefs({ selection: ScheduleItemKind.TRANSPORTATION.itemType });
   let fixedDurationMode = null;
   let onSelectRow = null;
   const zoomobileRow = {
      name: 'Zoomobile',
      route_duration_minutes: 75,
      scheduleItemKind: 'transportations',
   };
   const controller = createController({
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
   onSelectRow?.(zoomobileRow, 'Zoomobile');

   assert.deepEqual(fixedDurationMode, {
      lockDuration: true,
      durationMinutes: 75,
   });
});

test('Test_UpdateFieldVisibility_TestUpdateFieldVisibilityLocksDurationForTransportationAddedAsAn_ExpectOk', () => {
   const refs = createRefs({ selection: ScheduleItemKind.ATTRACTION.itemType });
   let fixedDurationMode = null;
   let onSelectRow = null;
   const zoomobileRow = {
      name: 'Zoomobile',
      added_as_attraction: true,
      route_duration_minutes: 75,
      scheduleItemKind: 'attractions',
   };
   const controller = createController({
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
   onSelectRow?.(zoomobileRow, 'Zoomobile');

   assert.deepEqual(fixedDurationMode, {
      lockDuration: true,
      durationMinutes: 75,
   });
});

test('Test_HandleTypeSelectChange_TestHandleTypeSelectChangeClearsTheSearchInputAndResetsTime_ExpectOk', () => {
   const refs = createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   let resetCount = 0;
   const controller = createController({
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

test('Test_HandleOnlyItineraryItemsChange_TestHandleOnlyItineraryItemsChangeReFiltersCachedSearchRows_ExpectOk', () => {
   const refs = createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
   });
   const renderedRows = [];
   const controller = createController({
      refs,
      deps: {
         renderSearchResults: ({ rows }) => {
            renderedRows.push(rows);
         },
      },
   });

   controller.displaySearchResults([
      ANIMAL_ROW,
      {
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         scheduleItemKind: 'animals',
      },
   ]);
   refs.onlyItineraryItemsCheckbox.checked = true;
   controller.handleOnlyItineraryItemsChange();

   assert.deepEqual(renderedRows.at(-1), [ANIMAL_ROW]);
});

test('Test_RenderSearchResultsForRows_TestRenderSearchResultsForRowsClearsResultsWhenSearchIsDisabled_ExpectOk', () => {
   const refs = createRefs({ selection: 'lunch' });
   refs.resultsEl.appendChild(createDomNode('div', 'existing-result'));
   const controller = createController({ refs });

   controller.displaySearchResults([ANIMAL_ROW]);

   assert.equal(refs.resultsEl.children.length, 0);
});

test('Test_RunSearch_TestRunSearchClearsResultsWhenSearchIsDisabledOr_ExpectOk', async () => {
   const refs = createRefs({ selection: 'lunch', searchValue: 'tiger' });
   refs.resultsEl.appendChild(createDomNode('div', 'existing-result'));
   const controller = createController({ refs });

   await controller.runSearch();

   assert.equal(refs.resultsEl.children.length, 0);

   refs.typeSelect.value = ScheduleItemKind.ANIMAL.itemType;
   refs.searchInput.value = '';
   await controller.runSearch();

   assert.equal(refs.resultsEl.children.length, 0);
});

test('Test_RunSearch_TestRunSearchSwallowsSearchFailuresAndClearsVisibleRows_ExpectOk', async () => {
   const refs = createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   const renderedRows = [];
   const controller = createController({
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

test('Test_HandleSchedule_TestHandleScheduleShowsResolvedErrorNoticesAndGenericFailures_ExpectOk', async () => {
   const refs = createRefs({ selection: 'lunch' });
   const notices = [];
   const controller = createController({
      refs,
      scheduleTimeFields: {
         getScheduleTimeOptions: () => ({}),
      },
      deps: {
         scheduleSelectedItem: async () => ({ errorType: 'validationError' }),
         itinerarySuccess: () => false,
         requiresNotOnItineraryConfirmation: () => false,
         resolveErrorMessage: () => 'Validation failed',
         showNotice: (message) => {
            notices.push(message);
         },
      },
   });

   await controller.handleSchedule();

   assert.deepEqual(notices, ['Validation failed']);

   const failingController = createController({
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

   await failingController.handleSchedule();

   assert.equal(notices.at(-1), Strings.itinerary.errors.generic);
});

test('Test_HandleSchedule_TestHandleScheduleReturnsSilentlyForNotOnItineraryConfirmations_ExpectOk', async () => {
   const refs = createRefs({ selection: 'lunch' });
   const notices = [];
   const controller = createController({
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

test('Test_HandleSchedule_TestHandleScheduleIgnoresDuplicateSubmissionsWhileOneIsIn_ExpectOk', async () => {
   const refs = createRefs({ selection: 'lunch' });
   let scheduleCalls = 0;
   let resolveSchedule = null;
   const controller = createController({
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

test('Test_Clicking_TestClickingThePreselectedResultDoesNotClearThe_ExpectOk', () => {
   const refs = createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'Tiger',
   });
   let onSelectRow = null;
   const controller = createController({
      refs,
      preselectedRow: ANIMAL_ROW,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });

   controller.initialize();
   onSelectRow?.(ANIMAL_ROW, 'Tiger||Savanna');

   assert.equal(controller.canScheduleSelection(), true);
});

test('Test_HandleSearchInput_TestHandleSearchInputClearsTheSelectedRowAndTriggersA_ExpectOk', () => {
   const refs = createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   const searchCalls = [];
   let onSelectRow = null;
   const controller = createController({
      refs,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });

   controller.displaySearchResults([ANIMAL_ROW]);
   onSelectRow?.(ANIMAL_ROW, 'Tiger||Savanna');
   controller.handleSearchInput(() => {
      searchCalls.push('search');
   });

   assert.equal(controller.canScheduleSelection(), false);
   assert.deepEqual(searchCalls, ['search']);
});

test('Test_HandleOnlyItineraryItemsChange_TestHandleOnlyItineraryItemsChangeRunsASearchWhenNoRowsAre_ExpectOk', async () => {
   const refs = createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
      searchValue: 'tiger',
   });
   const searchRequests = [];
   const controller = createController({
      refs,
      deps: {
         getSearchContext: async () => ({}),
         searchItineraryItems: async (_url, payload) => {
            searchRequests.push(payload);
            return { animals: [ANIMAL_ROW] };
         },
         renderSearchResults: () => {},
      },
   });

   refs.onlyItineraryItemsCheckbox.checked = true;
   await controller.handleOnlyItineraryItemsChange();

   assert.equal(searchRequests.length, 1);
});

test('Test_Initialize_TestInitializeWithoutAPreselectedRowClearsSearchResults_ExpectOk', () => {
   const refs = createRefs({ selection: ScheduleItemKind.ANIMAL.itemType });
   refs.resultsEl.appendChild(createDomNode('div', 'existing-result'));
   const controller = createController({ refs });

   controller.initialize();

   assert.equal(refs.resultsEl.children.length, 0);
   assert.equal(refs.scheduleButton.disabled, true);
});

test('Test_BindEvents_TestBindEventsWiresScheduleAndSearchInputHandlers_ExpectOk', async () => {
   const refs = createRefs({ selection: 'lunch' });
   let dismissed = false;
   const controller = createController({
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

   refs.typeSelect.value = ScheduleItemKind.ANIMAL.itemType;
   refs.typeSelect.listeners.change?.();
   refs.searchInput.listeners.input?.();

   assert.equal(refs.searchInput.value, '');
});

test('Test_DisplaySearchResults_TestDisplaySearchResultsClearsASelectedRowHiddenByItinerary_ExpectOk', () => {
   const refs = createRefs({
      selection: ScheduleItemKind.ANIMAL.itemType,
   });
   let onSelectRow = null;
   const controller = createController({
      refs,
      deps: {
         renderSearchResults: ({ onSelectRow: selectRow }) => {
            onSelectRow = selectRow;
         },
      },
   });

   controller.displaySearchResults([
      ANIMAL_ROW,
      {
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         scheduleItemKind: 'animals',
      },
   ]);
   onSelectRow?.({
      species: 'Giant Panda',
      exhibit: 'Bamboo',
      scheduleItemKind: 'animals',
   }, 'Giant Panda||Bamboo');

   refs.onlyItineraryItemsCheckbox.checked = true;
   controller.handleOnlyItineraryItemsChange();

   assert.equal(controller.canScheduleSelection(), false);
});
