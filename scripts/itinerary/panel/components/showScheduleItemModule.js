import { searchItineraryItems } from '../../../api/searchApi.js';
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
import {
   buildScheduleItemModuleBody,
   buildSearchRowRenderer,
} from './scheduleItemModuleForm.js';
import { renderScheduleItemSearchResults } from '../scheduleItemResults.js';
import {
   buildScheduleItemSearchPayload,
   extractScheduleItemSearchRows,
   filterScheduleItemRowsToItinerary,
   getScheduleItemRowId,
   getScheduleItemRowKind,
   resolveEffectiveScheduleItemSelection,
} from '../scheduleItemSearch.js';
import {
   isScheduleItemEventType,
   isScheduleItemSearchEnabled,
   isScheduleItemTypeUnset,
} from '../scheduleItemTypes.js';
import { getAnimalSpecies } from '../../selectors/animalSelector/model.js';
import { getAttractionTitle } from '../../selectors/attractionSelector/model.js';
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
