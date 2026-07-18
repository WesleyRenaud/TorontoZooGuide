import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { createScheduleItemModuleController } from '../../scripts/itinerary/panel/components/scheduleItemModuleController.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';

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
   return createScheduleItemModuleController({
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

test('updateFieldVisibility disables search for event-type selections', () => {
   const refs = createRefs({ selection: 'lunch' });
   const controller = createController({ refs });

   controller.updateFieldVisibility();

   assert.equal(refs.searchInput.disabled, true);
   assert.equal(refs.searchInput.getAttribute('aria-disabled'), 'true');
   assert.equal(refs.onlyItineraryItemsWrap.hidden, true);
   assert.equal(refs.scheduleButton.disabled, false);
});

test('updateFieldVisibility keeps the schedule button disabled until a row is selected', () => {
   const refs = createRefs({ selection: ScheduleItemKind.ANIMAL.itemType });
   const controller = createController({ refs });

   controller.updateFieldVisibility();

   assert.equal(refs.searchInput.disabled, false);
   assert.equal(refs.scheduleButton.disabled, true);
});

test('displaySearchResults filters rows to itinerary items when enabled', () => {
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

test('runSearch fetches rows and ignores stale responses', async () => {
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

test('handleSchedule allows duration without a start time', async () => {
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

test('handleSchedule dismisses the popup after a successful schedule', async () => {
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

test('applyPreselectedRow seeds the type, search input, and selected row', () => {
   const refs = createRefs();
   const controller = createScheduleItemModuleController({
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
});

test('displaySearchResults selects a row and infers the module type from the row kind', () => {
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

test('displaySearchResults clears the selection when the same row is chosen again', () => {
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

test('updateFieldVisibility disables time fields for selected talks and encounters', () => {
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
         reset: () => {
            fixedTimeMode = { enabled: false };
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

   assert.deepEqual(fixedTimeMode, { enabled: true });

   controller.handleTypeSelectChange();

   assert.deepEqual(fixedTimeMode, { enabled: false });
});

test('handleTypeSelectChange clears the search input and resets time fields', () => {
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

test('handleOnlyItineraryItemsChange re-filters cached search rows', () => {
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

test('renderSearchResultsForRows clears results when search is disabled', () => {
   const refs = createRefs({ selection: 'lunch' });
   refs.resultsEl.appendChild(createDomNode('div', 'existing-result'));
   const controller = createController({ refs });

   controller.displaySearchResults([ANIMAL_ROW]);

   assert.equal(refs.resultsEl.children.length, 0);
});

test('runSearch clears results when search is disabled or the query is blank', async () => {
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

test('runSearch swallows search failures and clears visible rows', async () => {
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

test('handleSchedule shows resolved error notices and generic failures', async () => {
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

   assert.equal(notices.at(-1), APP_STRINGS.itinerary.errors.generic);
});

test('handleSchedule returns silently for not-on-itinerary confirmations', async () => {
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

test('handleSchedule ignores duplicate submissions while one is in flight', async () => {
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

test('handleSearchInput clears the selected row and triggers a search', () => {
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

test('handleOnlyItineraryItemsChange runs a search when no rows are cached', async () => {
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

test('initialize without a preselected row clears search results', () => {
   const refs = createRefs({ selection: ScheduleItemKind.ANIMAL.itemType });
   refs.resultsEl.appendChild(createDomNode('div', 'existing-result'));
   const controller = createController({ refs });

   controller.initialize();

   assert.equal(refs.resultsEl.children.length, 0);
   assert.equal(refs.scheduleButton.disabled, true);
});

test('bindEvents wires schedule and search input handlers', async () => {
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

test('displaySearchResults clears a selected row hidden by itinerary-only filtering', () => {
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
