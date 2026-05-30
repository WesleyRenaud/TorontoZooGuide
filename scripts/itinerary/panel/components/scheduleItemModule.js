import { searchItineraryItems } from '../../../api/searchApi.js';
import { el } from '../dom.js';
import { getItineraryDateSearchContext } from '../../itinerarySearchContext.js';
import {
   createItineraryPopupLayout,
   getItineraryPanelMountEl,
   mountDismissablePopup,
} from './popup.js';
import {
   addAnimalToItinerary,
   addAttractionToItinerary,
} from '../scheduleItemActions.js';
import { renderScheduleItemSearchResults } from '../scheduleItemResults.js';
import {
   buildScheduleItemSearchPayload,
   extractScheduleItemSearchRows,
   getScheduleItemRowId,
   getScheduleItemRowKind,
} from '../scheduleItemSearch.js';
import {
   buildScheduleItemTypeOptions,
   isScheduleItemEventType,
   isScheduleItemSearchEnabled,
   isScheduleItemTypeUnset,
   SCHEDULE_ITEM_MODULE_TYPES,
} from '../scheduleItemTypes.js';
import {
   buildAnimalImageSrc,
   getAnimalSpecies,
   getAnimalSubtitle,
} from '../../selectors/animalSelector/model.js';
import {
   buildAttractionImageSrc,
   getAttractionInfoLink,
   getAttractionSubtitle,
   getAttractionTitle,
} from '../../selectors/attractionSelector/model.js';
import { createDefaultSelectorRowLeftRenderer } from '../../selectors/base/resultRenderer.js';
import { APP_STRINGS } from '../../../strings.js';

const SEARCH_DEBOUNCE_MS = 250;

function debounce(fn, delay = SEARCH_DEBOUNCE_MS) {
   let timeoutId = null;

   return (...args) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn(...args), delay);
   };
}

function createFieldLabel(text) {
   return el('label', 'schedule-item-field-label', text);
}

function createSelectField({
   label,
   options = [],
   getOptionValue = (option) => option,
   getOptionLabel = (option) => String(option),
} = {}) {
   const field = el('div', 'schedule-item-field');
   const select = document.createElement('select');
   select.className = 'schedule-item-select';

   field.appendChild(createFieldLabel(label));
   field.appendChild(select);

   options.forEach((option) => {
      const optionEl = document.createElement('option');
      const value = getOptionValue(option);

      optionEl.value = value;
      optionEl.textContent = getOptionLabel(option);
      optionEl.selected = Boolean(option.selected);
      select.appendChild(optionEl);
   });

   return {
      field,
      select,
   };
}

function buildSearchRowRenderer(moduleType) {
   if (moduleType === SCHEDULE_ITEM_MODULE_TYPES.animals) {
      return createDefaultSelectorRowLeftRenderer({
         getTitle: getAnimalSpecies,
         getSubtitle: getAnimalSubtitle,
         getImageSrc: buildAnimalImageSrc,
         getInfoLink: () => null,
      });
   }

   return createDefaultSelectorRowLeftRenderer({
      getTitle: getAttractionTitle,
      getSubtitle: getAttractionSubtitle,
      getImageSrc: buildAttractionImageSrc,
      getInfoLink: getAttractionInfoLink,
   });
}

function buildScheduleItemModuleBody(strings, eventTypes = []) {
   const body = el('div', 'schedule-item-module-body');

   const typeField = createSelectField({
      label: strings.typeLabel,
      options: buildScheduleItemTypeOptions(eventTypes, strings),
      getOptionValue: (option) => option.value,
      getOptionLabel: (option) => option.label,
   });

   const searchField = el('div', 'schedule-item-field schedule-item-search-field');
   const searchLabelEl = createFieldLabel(strings.searchLabel);
   const searchInput = document.createElement('input');
   searchInput.className = 'schedule-item-search-input';
   searchInput.type = 'text';
   searchInput.placeholder = strings.searchPlaceholder;
   searchInput.autocomplete = 'off';

   searchField.append(searchLabelEl, searchInput);

   const resultsEl = el('div', 'itin-results schedule-item-results');
   resultsEl.setAttribute('aria-live', 'polite');

   body.append(typeField.field, searchField, resultsEl);

   return {
      body,
      typeSelect: typeField.select,
      searchInput,
      resultsEl,
   };
}

export function showScheduleItemModule({
   itinerary = {},
   eventTypes = [],
   onScheduled = null,
   onScheduleGeneric = null,
} = {}) {
   const strings = APP_STRINGS.itinerary.scheduleItem;
   const { body: moduleBodyEl } = buildScheduleItemModuleBody(strings, eventTypes);
   const {
      root,
      overlay,
      buttonEls,
      closeButton,
   } = createItineraryPopupLayout({
      popupClassName: 'schedule-item-module',
      title: strings.title,
      bodyContent: moduleBodyEl,
      showCloseButton: true,
      actionButtons: [
         {
            key: 'cancel',
            className: 'itin-prev',
            text: APP_STRINGS.itinerary.actions.cancel,
         },
         {
            key: 'schedule',
            className: 'itin-finish',
            text: strings.scheduleButton,
         },
      ],
   });

   const body = root.querySelector('.schedule-item-module-body');
   const typeSelect = body?.querySelector('.schedule-item-select');
   const searchInput = body?.querySelector('.schedule-item-search-input');
   const resultsEl = body?.querySelector('.schedule-item-results');
   const searchLabelEl = body?.querySelector('.schedule-item-search-field .schedule-item-field-label');

   let selectedRowId = '';
   let selectedRow = null;
   let latestSearchRequestId = 0;
   let isSubmitting = false;

   const renderAnimalRowLeft = buildSearchRowRenderer(SCHEDULE_ITEM_MODULE_TYPES.animals);
   const renderAttractionRowLeft = buildSearchRowRenderer(
      SCHEDULE_ITEM_MODULE_TYPES.attractions
   );

   function getSelection() {
      return typeSelect?.value ?? '';
   }

   function clearSelectedRow() {
      selectedRowId = '';
      selectedRow = null;
   }

   function canScheduleSelection() {
      const selection = getSelection();

      if (isScheduleItemTypeUnset(selection)) {
         return false;
      }

      if (isScheduleItemSearchEnabled(selection, eventTypes)) {
         return Boolean(selectedRow);
      }

      return isScheduleItemEventType(selection, eventTypes);
   }

   function updateFieldVisibility() {
      const selection = getSelection();
      const searchEnabled = isScheduleItemSearchEnabled(selection, eventTypes);

      if (searchInput) {
         searchInput.disabled = !searchEnabled;
         searchInput.setAttribute('aria-disabled', String(!searchEnabled));
      }

      if (searchLabelEl) {
         searchLabelEl.classList.toggle('is-disabled', !searchEnabled);
      }

      buttonEls.schedule.disabled = isSubmitting || !canScheduleSelection();
   }

   function renderSearchResultRowLeft(row) {
      const selection = getSelection();

      if (
         selection === SCHEDULE_ITEM_MODULE_TYPES.attractions
         || getScheduleItemRowKind(row) === SCHEDULE_ITEM_MODULE_TYPES.attractions
      ) {
         return renderAttractionRowLeft(row);
      }

      return renderAnimalRowLeft(row);
   }

   function renderSearchResults(rows) {
      const selection = getSelection();

      if (!isScheduleItemSearchEnabled(selection, eventTypes)) {
         resultsEl.replaceChildren();
         return;
      }

      renderScheduleItemSearchResults({
         resultsEl,
         rows,
         emptyText: strings.emptyResults,
         getId: getScheduleItemRowId,
         selectedRowId,
         renderRowLeft: renderSearchResultRowLeft,
         onSelectRow: (row, id) => {
            const isSameRow = id === selectedRowId;

            clearSelectedRow();

            if (!isSameRow) {
               selectedRowId = id;
               selectedRow = row;
            }

            renderSearchResults(rows);
            updateFieldVisibility();
         },
      });
   }

   function clearSearchResults() {
      resultsEl?.replaceChildren();
   }

   async function runSearch() {
      const selection = getSelection();

      if (!isScheduleItemSearchEnabled(selection, eventTypes)) {
         clearSearchResults();
         return;
      }

      const query = searchInput?.value?.trim() ?? '';

      if (!query) {
         clearSearchResults();
         return;
      }

      const requestId = ++latestSearchRequestId;

      try {
         const context = await getItineraryDateSearchContext();
         const response = await searchItineraryItems(
            '/search',
            {
               ...buildScheduleItemSearchPayload(selection, query),
               ...context,
            }
         );
         const rows = extractScheduleItemSearchRows(selection, response);

         if (requestId !== latestSearchRequestId) {
            return;
         }

         renderSearchResults(rows);
      }
      catch {
         if (requestId !== latestSearchRequestId) {
            return;
         }

         renderSearchResults([]);
      }
   }

   const scheduleSearch = debounce(() => {
      void runSearch();
   });

   async function handleSchedule() {
      if (isSubmitting || !canScheduleSelection()) {
         return;
      }

      const selection = getSelection();

      isSubmitting = true;
      updateFieldVisibility();

      try {
         if (isScheduleItemSearchEnabled(selection, eventTypes) && selectedRow) {
            if (getScheduleItemRowKind(selectedRow) === SCHEDULE_ITEM_MODULE_TYPES.attractions) {
               await addAttractionToItinerary(itinerary, selectedRow);
            }
            else {
               await addAnimalToItinerary(itinerary, selectedRow);
            }
         }
         else if (isScheduleItemEventType(selection, eventTypes)) {
            await onScheduleGeneric?.({ eventType: selection });
         }

         popup.dismiss();
         await onScheduled?.();
      }
      finally {
         isSubmitting = false;
      }
   }

   const popup = mountDismissablePopup({
      mountEl: getItineraryPanelMountEl() ?? document.body,
      root,
      overlay,
      initialFocusEl: typeSelect,
      onDismiss: null,
   });

   typeSelect?.addEventListener('change', () => {
      clearSelectedRow();
      if (searchInput) {
         searchInput.value = '';
      }
      updateFieldVisibility();
      void runSearch();
   });

   searchInput?.addEventListener('input', () => {
      clearSelectedRow();
      scheduleSearch();
      updateFieldVisibility();
   });

   buttonEls.cancel?.addEventListener('click', () => {
      popup.dismiss();
   });

   closeButton?.addEventListener('click', () => {
      popup.dismiss();
   });

   buttonEls.schedule?.addEventListener('click', () => {
      void handleSchedule();
   });

   updateFieldVisibility();
   clearSearchResults();

   return popup;
}
