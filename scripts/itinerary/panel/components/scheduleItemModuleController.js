import { SearchApi } from '../../../api/searchApi.js';
import { ItineraryConfirmationResult } from '../../itineraryConfirmationResult.js';
import { ItineraryErrorTypes } from '../../itineraryErrorTypes.js';
import { ItinerarySearchContext } from '../../itinerarySearchContext.js';
import { scheduleSelectedItineraryItem } from '../scheduleItemActions.js';
import { ScheduleItemModuleSelection } from './scheduleItemModuleSelection.js';
import { ScheduleItemResults } from '../scheduleItemResults.js';
import { ScheduleItemSearch } from '../scheduleItemSearch.js';
import { ScheduleItemTypes } from '../scheduleItemTypes.js';
import { TransportationSelectorModel } from '../../selectors/transportationSelector/transportationSelectorModel.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { ShowScheduleItemNotice } from '../showScheduleItemNotice.js';
import { APP_STRINGS } from '../../../strings.js';

export function createScheduleItemModuleController({
   itinerary = {},
   eventTypes = [],
   strings = {},
   preselectedRow = null,
   refs = {},
   scheduleTimeFields = {},
   scheduleButton = null,
   renderAnimalRowLeft = () => null,
   renderAttractionRowLeft = () => null,
   renderTransportationRowLeft = () => null,
   renderGuardiansTalkRowLeft = () => null,
   renderWildEncounterRowLeft = () => null,
   onScheduled = null,
   deps = {},
} = {}) {
   const {
      typeSelect = null,
      typeLabelEl = null,
      searchInput = null,
      resultsEl = null,
      searchLabelEl = null,
      onlyItineraryItemsCheckbox = null,
      onlyItineraryItemsWrap = null,
   } = refs;

   const {
      searchItineraryItems: searchItems = SearchApi.searchItineraryItems,
      getSearchContext = ItinerarySearchContext.getItineraryDateSearchContext,
      scheduleSelectedItem = scheduleSelectedItineraryItem,
      showNotice = ShowScheduleItemNotice.showScheduleItemNotice,
      renderSearchResults = ScheduleItemResults.renderScheduleItemSearchResults,
      itinerarySuccess = ItineraryErrorTypes.isItinerarySuccess,
      requiresNotOnItineraryConfirmation = ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation,
      resolveErrorMessage = ItineraryErrorTypes.resolveItineraryErrorMessage,
      genericErrorMessage = APP_STRINGS.itinerary.errors.generic,
   } = deps;

   let selectedRowId = '';
   let selectedRow = null;
   let latestSearchRows = [];
   let latestSearchRequestId = 0;
   let isSubmitting = false;

   function getSelection() {
      return typeSelect?.value ?? '';
   }

   function clearSelectedRow() {
      selectedRowId = '';
      selectedRow = null;
   }

   function canScheduleSelection() {
      return ScheduleItemModuleSelection.canScheduleModuleSelection({
         selection: getSelection(),
         selectedRow,
         eventTypes,
      });
   }

   function isOnlyItineraryItemsEnabled() {
      return Boolean(onlyItineraryItemsCheckbox?.checked);
   }

   function isItemSelectionLocked() {
      return Boolean(preselectedRow);
   }

   function syncScheduleTimeFields() {
      if (!selectedRow) {
         scheduleTimeFields.reset?.();
         return;
      }

      const rowKind = ScheduleItemSearch.getScheduleItemRowKind(selectedRow);

      if (ScheduleItemKind.isFixedTimeScheduleItemKind(rowKind)) {
         scheduleTimeFields.setFixedDurationScheduleMode?.({ lockDuration: false });
         scheduleTimeFields.setFixedTimeScheduleMode?.({ lockTimes: true });
         return;
      }

      if (TransportationSelectorModel.isScheduleItemTransportationRow(selectedRow)) {
         scheduleTimeFields.setFixedTimeScheduleMode?.({ lockTimes: false });
         scheduleTimeFields.setFixedDurationScheduleMode?.({
            lockDuration: true,
            durationMinutes: selectedRow.route_duration_minutes,
         });
         return;
      }

      scheduleTimeFields.reset?.();
   }

   function updateFieldVisibility() {
      const selection = getSelection();
      const searchEnabled = ScheduleItemTypes.isScheduleItemSearchEnabled(selection, eventTypes);
      const itemSelectionLocked = isItemSelectionLocked();
      const searchLocked = itemSelectionLocked || !searchEnabled;

      if (typeSelect) {
         typeSelect.disabled = itemSelectionLocked;
         typeSelect.setAttribute('aria-disabled', String(itemSelectionLocked));
      }

      if (typeLabelEl) {
         typeLabelEl.classList.toggle('is-disabled', itemSelectionLocked);
      }

      if (searchInput) {
         searchInput.disabled = searchLocked;
         searchInput.setAttribute('aria-disabled', String(searchLocked));
      }

      if (searchLabelEl) {
         searchLabelEl.classList.toggle('is-disabled', searchLocked);
      }

      if (onlyItineraryItemsWrap) {
         onlyItineraryItemsWrap.hidden = !searchEnabled;
      }

      if (onlyItineraryItemsCheckbox) {
         onlyItineraryItemsCheckbox.disabled = searchLocked;
      }

      if (scheduleButton) {
         scheduleButton.disabled = isSubmitting || !canScheduleSelection();
      }

      syncScheduleTimeFields();
   }

   function renderSearchResultsForRows(rows) {
      const selection = getSelection();

      if (!ScheduleItemTypes.isScheduleItemSearchEnabled(selection, eventTypes)) {
         resultsEl?.replaceChildren();
         return;
      }

      renderSearchResults({
         resultsEl,
         rows,
         emptyText: strings.emptyResults,
         getId: ScheduleItemSearch.getScheduleItemRowId,
         selectedRowId,
         renderRowLeft: (row) => ScheduleItemModuleSelection.resolveScheduleModuleSearchRowRenderer({
            row,
            renderAnimalRowLeft,
            renderAttractionRowLeft,
            renderTransportationRowLeft,
            renderGuardiansTalkRowLeft,
            renderWildEncounterRowLeft,
         }),
         onSelectRow: (row, id) => {
            if (isItemSelectionLocked()) {
               return;
            }

            const isSameRow = id === selectedRowId;

            clearSelectedRow();

            if (!isSameRow) {
               selectedRowId = id;
               selectedRow = row;

               if (typeSelect && ScheduleItemTypes.isScheduleItemTypeUnset(getSelection())) {
                  typeSelect.value = ScheduleItemSearch.getScheduleItemRowKind(row);
               }
            }

            renderSearchResultsForRows(rows);
            updateFieldVisibility();
         },
      });
   }

   function displaySearchResults(rows = []) {
      latestSearchRows = rows;
      const visibleRows = ScheduleItemModuleSelection.filterVisibleScheduleModuleRows({
         rows,
         itinerary,
         onlyItineraryItemsEnabled: isOnlyItineraryItemsEnabled(),
      });

      if (ScheduleItemModuleSelection.shouldClearSelectedScheduleRow({ selectedRowId, visibleRows })) {
         clearSelectedRow();
      }

      renderSearchResultsForRows(visibleRows);
   }

   function clearSearchResults() {
      resultsEl?.replaceChildren();
   }

   function applyPreselectedRow() {
      if (!preselectedRow) {
         return;
      }

      selectedRowId = ScheduleItemSearch.getScheduleItemRowId(preselectedRow);
      selectedRow = preselectedRow;

      if (typeSelect) {
         typeSelect.value = ScheduleItemSearch.getScheduleItemRowKind(preselectedRow);
      }

      if (searchInput) {
         searchInput.value = ScheduleItemModuleSelection.resolveScheduleModuleSearchLabel(preselectedRow);
      }

      displaySearchResults([preselectedRow]);
      updateFieldVisibility();
   }

   async function runSearch() {
      const selection = getSelection();

      if (!ScheduleItemTypes.isScheduleItemSearchEnabled(selection, eventTypes)) {
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
         const context = await getSearchContext();
         const response = await searchItems(
            '/search',
            {
               ...ScheduleItemSearch.buildScheduleItemSearchPayload(selection, query),
               ...context,
            }
         );
         const rows = ScheduleItemSearch.extractScheduleItemSearchRows(selection, response);

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

   async function handleSchedule({ dismissPopup = null } = {}) {
      if (isSubmitting || !canScheduleSelection()) {
         return;
      }

      const selection = ScheduleItemSearch.resolveEffectiveScheduleItemSelection(getSelection(), selectedRow);
      const scheduleOptions = scheduleTimeFields.getScheduleTimeOptions?.() ?? {};

      isSubmitting = true;
      updateFieldVisibility();

      try {
         const result = await scheduleSelectedItem(
            itinerary,
            selection,
            selectedRow,
            eventTypes,
            scheduleOptions
         );

         if (ItineraryConfirmationResult.isItineraryConfirmationCancelled(result)) {
            return;
         }

         if (
            !itinerarySuccess(result.errorType)
            && !requiresNotOnItineraryConfirmation(result.errorType)
         ) {
            showNotice(resolveErrorMessage(result.errorType));
            return;
         }

         if (!itinerarySuccess(result.errorType)) {
            return;
         }

         dismissPopup?.();
         await onScheduled?.();
      }
      catch {
         showNotice(genericErrorMessage);
      }
      finally {
         isSubmitting = false;
         updateFieldVisibility();
      }
   }

   function handleTypeSelectChange() {
      clearSelectedRow();

      if (searchInput) {
         searchInput.value = '';
      }

      updateFieldVisibility();
      void runSearch();
   }

   function handleSearchInput(scheduleSearch) {
      clearSelectedRow();
      scheduleSearch?.();
      updateFieldVisibility();
   }

   function handleOnlyItineraryItemsChange() {
      if (latestSearchRows.length > 0) {
         displaySearchResults(latestSearchRows);
      }
      else {
         void runSearch();
      }

      updateFieldVisibility();
   }

   function initialize() {
      if (preselectedRow) {
         applyPreselectedRow();
         return;
      }

      updateFieldVisibility();
      clearSearchResults();
   }

   function bindEvents({
      popup = null,
      scheduleSearch = null,
   } = {}) {
      typeSelect?.addEventListener('change', handleTypeSelectChange);
      searchInput?.addEventListener('input', () => {
         handleSearchInput(scheduleSearch);
      });
      onlyItineraryItemsCheckbox?.addEventListener('change', handleOnlyItineraryItemsChange);
      scheduleButton?.addEventListener('click', () => {
         void handleSchedule({ dismissPopup: () => popup?.dismiss?.() });
      });
   }

   return {
      applyPreselectedRow,
      bindEvents,
      canScheduleSelection,
      clearSearchResults,
      displaySearchResults,
      handleSchedule,
      handleOnlyItineraryItemsChange,
      handleSearchInput,
      handleTypeSelectChange,
      initialize,
      runSearch,
      updateFieldVisibility,
   };
}
