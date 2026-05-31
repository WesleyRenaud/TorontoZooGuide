import { searchItineraryItems } from '../../../api/searchApi.js';
import { el } from '../dom.js';
import {
   isItinerarySuccess,
   requiresScheduleItemNotOnItineraryConfirmation,
   resolveItineraryErrorMessage,
} from '../../itineraryErrorTypes.js';
import { getItineraryDateSearchContext } from '../../itinerarySearchContext.js';
import {
   createItineraryPopupLayout,
   getItineraryPanelMountEl,
   mountDismissablePopup,
} from './popup.js';
import { scheduleSelectedItineraryItem } from '../scheduleItemActions.js';
import { renderScheduleItemSearchResults } from '../scheduleItemResults.js';
import {
   buildScheduleItemSearchPayload,
   extractScheduleItemSearchRows,
   filterScheduleItemRowsToItinerary,
   getScheduleItemRowId,
   getScheduleItemRowKind,
   resolveEffectiveScheduleItemSelection,
} from '../scheduleItemSearch.js';
import { makeScheduleItemTimeFields } from './scheduleItemTimeFields.js';
import {
   buildScheduleItemTypeOptions,
   isScheduleItemEventType,
   isScheduleItemSearchEnabled,
   isScheduleItemTypeUnset,
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
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { showScheduleItemNotice } from '../showScheduleItemNotice.js';
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

function createOnlyItineraryItemsCheckbox(labelText) {
   const wrap = el('div', 'schedule-item-only-itinerary-wrap');
   const label = el('label', 'schedule-item-only-itinerary-row');
   const checkbox = document.createElement('input');

   checkbox.type = 'checkbox';
   checkbox.className = 'schedule-item-only-itinerary-checkbox';
   checkbox.checked = false;

   const text = el('span', 'schedule-item-only-itinerary-label', labelText);
   label.append(checkbox, text);
   wrap.appendChild(label);

   return { wrap, checkbox };
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
   if (moduleType === ScheduleItemKind.ANIMAL.itemType) {
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

   const onlyItineraryItemsField = createOnlyItineraryItemsCheckbox(
      strings.onlyItineraryItemsLabel
   );

   searchField.append(searchLabelEl, searchInput);

   const resultsEl = el('div', 'itin-results schedule-item-results');
   resultsEl.setAttribute('aria-live', 'polite');
   const scheduleTimeFields = makeScheduleItemTimeFields(strings);

   body.append(
      typeField.field,
      searchField,
      onlyItineraryItemsField.wrap,
      ...scheduleTimeFields.fields,
      resultsEl
   );

   return {
      body,
      typeSelect: typeField.select,
      searchInput,
      onlyItineraryItemsCheckbox: onlyItineraryItemsField.checkbox,
      resultsEl,
      scheduleTimeFields,
   };
}

export function showScheduleItemModule({
   itinerary = {},
   eventTypes = [],
   onScheduled = null,
   preselectedRow = null,
} = {}) {
   const strings = APP_STRINGS.itinerary.scheduleItem;
   const {
      body: moduleBodyEl,
      scheduleTimeFields,
   } = buildScheduleItemModuleBody(strings, eventTypes);
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
   const onlyItineraryItemsCheckbox = body?.querySelector(
      '.schedule-item-only-itinerary-checkbox'
   );
   const onlyItineraryItemsWrap = body?.querySelector('.schedule-item-only-itinerary-wrap');

   let selectedRowId = '';
   let selectedRow = null;
   let latestSearchRows = [];
   let latestSearchRequestId = 0;
   let isSubmitting = false;

   const renderAnimalRowLeft = buildSearchRowRenderer(ScheduleItemKind.ANIMAL.itemType);
   const renderAttractionRowLeft = buildSearchRowRenderer(
      ScheduleItemKind.ATTRACTION.itemType
   );

   function getSelection() {
      return typeSelect?.value ?? '';
   }

   function getEffectiveSelection() {
      return resolveEffectiveScheduleItemSelection(getSelection(), selectedRow);
   }

   function clearSelectedRow() {
      selectedRowId = '';
      selectedRow = null;
   }

   function canScheduleSelection() {
      const selection = getEffectiveSelection();

      if (isScheduleItemTypeUnset(selection)) {
         return false;
      }

      if (isScheduleItemSearchEnabled(selection, eventTypes)) {
         return Boolean(selectedRow);
      }

      return isScheduleItemEventType(selection, eventTypes);
   }

   function isOnlyItineraryItemsEnabled() {
      return Boolean(onlyItineraryItemsCheckbox?.checked);
   }

   function applyItineraryItemFilter(rows = []) {
      if (!isOnlyItineraryItemsEnabled()) {
         return rows;
      }

      return filterScheduleItemRowsToItinerary(rows, itinerary);
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

      if (onlyItineraryItemsWrap) {
         onlyItineraryItemsWrap.hidden = !searchEnabled;
      }

      if (onlyItineraryItemsCheckbox) {
         onlyItineraryItemsCheckbox.disabled = !searchEnabled;
      }

      buttonEls.schedule.disabled = isSubmitting || !canScheduleSelection();
   }

   function displaySearchResults(rows = []) {
      latestSearchRows = rows;
      const visibleRows = applyItineraryItemFilter(rows);

      if (
         selectedRowId
         && !visibleRows.some((row) => getScheduleItemRowId(row) === selectedRowId)
      ) {
         clearSelectedRow();
      }

      renderSearchResults(visibleRows);
   }

   function renderSearchResultRowLeft(row) {
      const selection = getSelection();

      if (
         selection === ScheduleItemKind.ATTRACTION.itemType
         || getScheduleItemRowKind(row) === ScheduleItemKind.ATTRACTION.itemType
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

               if (typeSelect && isScheduleItemTypeUnset(getSelection())) {
                  typeSelect.value = getScheduleItemRowKind(row);
               }
            }

            renderSearchResults(rows);
            updateFieldVisibility();
         },
      });
   }

   function clearSearchResults() {
      resultsEl?.replaceChildren();
   }

   function applyPreselectedRow() {
      if (!preselectedRow) {
         return;
      }

      selectedRowId = getScheduleItemRowId(preselectedRow);
      selectedRow = preselectedRow;

      if (typeSelect) {
         typeSelect.value = getScheduleItemRowKind(preselectedRow);
      }

      if (searchInput) {
         const searchLabel = getScheduleItemRowKind(preselectedRow)
            === ScheduleItemKind.ATTRACTION.itemType
            ? getAttractionTitle(preselectedRow)
            : getAnimalSpecies(preselectedRow);

         searchInput.value = searchLabel || '';
      }

      displaySearchResults([preselectedRow]);
      updateFieldVisibility();
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

         displaySearchResults(rows);
      }
      catch {
         if (requestId !== latestSearchRequestId) {
            return;
         }

         displaySearchResults([]);
      }
   }

   const scheduleSearch = debounce(() => {
      void runSearch();
   });

   async function handleSchedule() {
      if (isSubmitting || !canScheduleSelection()) {
         return;
      }

      if (scheduleTimeFields.hasDurationWithoutTime()) {
         showScheduleItemNotice(strings.durationRequiresTime);
         return;
      }

      const selection = getEffectiveSelection();
      const scheduleOptions = scheduleTimeFields.getScheduleTimeOptions();

      isSubmitting = true;
      updateFieldVisibility();

      try {
         const result = await scheduleSelectedItineraryItem(
            itinerary,
            selection,
            selectedRow,
            eventTypes,
            scheduleOptions
         );

         if (
            !isItinerarySuccess(result.errorType)
            && !requiresScheduleItemNotOnItineraryConfirmation(result.errorType)
         ) {
            showScheduleItemNotice(resolveItineraryErrorMessage(result.errorType));
            return;
         }

         if (!isItinerarySuccess(result.errorType)) {
            return;
         }

         popup.dismiss();
         await onScheduled?.();
      }
      catch {
         showScheduleItemNotice(APP_STRINGS.itinerary.errors.generic);
      }
      finally {
         isSubmitting = false;
         updateFieldVisibility();
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
      scheduleTimeFields.reset();
      updateFieldVisibility();
      void runSearch();
   });

   searchInput?.addEventListener('input', () => {
      clearSelectedRow();
      scheduleSearch();
      updateFieldVisibility();
   });

   onlyItineraryItemsCheckbox?.addEventListener('change', () => {
      if (latestSearchRows.length > 0) {
         displaySearchResults(latestSearchRows);
      }
      else {
         void runSearch();
      }

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

   if (preselectedRow) {
      applyPreselectedRow();
   }
   else {
      updateFieldVisibility();
      clearSearchResults();
   }

   return popup;
}
