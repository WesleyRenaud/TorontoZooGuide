import { searchItineraryItems } from '../../api/searchApi.js';
import { createSelectorSelectionState } from './base/selectionState.js';
import {
   createDefaultSelectorRowLeftRenderer,
   renderSelectorResults,
} from './base/resultRenderer.js';
import { buildSelectorShell } from './base/shell.js';

const SEARCH_DEBOUNCE_MS = 250;

function debounce(fn, delay = 250) {
   let timeoutId = null;

   return (...args) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn(...args), delay);
   };
}

function defaultMigrate(items) {
   return items;
}

function validateSelectorConfig({
   storageKey,
   getId,
   extractRows,
} = {}) {
   if (!storageKey) {
      throw new Error('createItinerarySelectorController: storageKey is required');
   }

   if (typeof getId !== 'function') {
      throw new Error('createItinerarySelectorController: getId(row) is required');
   }

   if (typeof extractRows !== 'function') {
      throw new Error('createItinerarySelectorController: extractRows(response) is required');
   }
}

function createSelectorElements({
   topTitle,
   h1,
   subtitle,
   hideNextButton,
} = {}) {
   const shell = buildSelectorShell({
      topTitle,
      h1,
      subtitle,
      hideNextButton,
   });

   return {
      rootEl: shell.root,
      bodyEl: shell.bodyEl,
      inputEl: shell.inputEl,
      resultsEl: shell.resultsEl,
      prevButtonEl: shell.prevButton,
      nextButtonEl: shell.nextButton,
      finishButtonEl: shell.finishButton,
      closeButtonEl: shell.closeButton,
   };
}

function createSelectorSearchRunner({
   searchEndpoint,
   buildSearchPayload,
   extractRows,
   getContext,
   getQuery,
   onRows,
} = {}) {
   let latestSearchRequestId = 0;

   async function fetchRows(query) {
      const context = typeof getContext === 'function'
         ? await getContext()
         : {};

      const response = await searchItineraryItems(searchEndpoint, {
         ...buildSearchPayload(query),
         ...context,
      });

      return extractRows(response);
   }

   async function runCurrentQuery() {
      const requestId = ++latestSearchRequestId;
      const query = getQuery()?.trim() ?? '';

      try {
         const rows = await fetchRows(query);

         if (requestId !== latestSearchRequestId) {
            return;
         }

         onRows(rows);
      }
      catch {
         if (requestId !== latestSearchRequestId) {
            return;
         }

         onRows([]);
      }
   }

   const scheduleCurrentQuery = debounce(() => {
      void runCurrentQuery();
   }, SEARCH_DEBOUNCE_MS);

   return {
      runCurrentQuery,
      scheduleCurrentQuery,
   };
}

export function createItinerarySelectorController({
   mountEl,

   onPrev,
   onNext,
   onFinish,
   onClose,
   hideNextButton = false,

   storageKey,
   migrateSelected = defaultMigrate,

   searchEndpoint = '/search',
   buildSearchPayload = query => ({ query }),
   extractRows,

   getContext = null,

   getId,
   getTitle = () => '',
   getSubtitle = () => '',
   getImageSrc = () => null,
   getInfoLink = () => null,

   makeSelection = row => ({ id: getId(row) }),

   topTitle = 'Itinerary Builder',
   h1 = 'Add Items',
   subtitle = 'Search and add items to your plan.',
   emptyText = 'No results found.',

   renderRowLeft,
   renderExtraControls = null,

   onBeforeToggleAdd = null,
} = {}) {
   validateSelectorConfig({
      storageKey,
      getId,
      extractRows,
   });

   let elements = null;

   const selectionState = createSelectorSelectionState({
      storageKey,
      migrateSelected,
      getId,
      makeSelection,
   });

   const resolvedRenderRowLeft = renderRowLeft
      || createDefaultSelectorRowLeftRenderer({
         getTitle,
         getSubtitle,
         getImageSrc,
         getInfoLink,
      });

   function getSelectionSnapshot() {
      return selectionState.getSelectedSnapshot();
   }

   function renderRows(rows) {
      if (!elements?.resultsEl) {
         return;
      }

      renderSelectorResults({
         resultsEl: elements.resultsEl,
         rows,
         emptyText,
         getId,
         isSelected: selectionState.isSelected,
         renderRowLeft: resolvedRenderRowLeft,
         onToggle: selectionState.toggleRow,
         onBeforeToggleAdd,
      });
   }

   const searchRunner = createSelectorSearchRunner({
      searchEndpoint,
      buildSearchPayload,
      extractRows,
      getContext,
      getQuery: () => elements?.inputEl?.value ?? '',
      onRows: renderRows,
   });

   function handlePrev() {
      onPrev?.();
   }

   function handleNext() {
      onNext?.(getSelectionSnapshot());
   }

   function handleFinish() {
      onFinish?.(getSelectionSnapshot());
   }

   function handleClose() {
      onClose?.();
   }

   function bindEvents() {
      elements?.inputEl?.addEventListener('input', searchRunner.scheduleCurrentQuery);
      elements?.prevButtonEl?.addEventListener('click', handlePrev);
      elements?.nextButtonEl?.addEventListener('click', handleNext);
      elements?.finishButtonEl?.addEventListener('click', handleFinish);
      elements?.closeButtonEl?.addEventListener('click', handleClose);
   }

   function renderExtraUi() {
      if (typeof renderExtraControls !== 'function' || !elements) {
         return;
      }

      renderExtraControls({
         rootEl: elements.rootEl,
         bodyEl: elements.bodyEl,
         inputEl: elements.inputEl,
         resultsEl: elements.resultsEl,
         rerunSearch: () => {
            void searchRunner.runCurrentQuery();
         },
      });
   }

   function ensureBuilt() {
      if (elements) {
         return;
      }

      elements = createSelectorElements({
         topTitle,
         h1,
         subtitle,
         hideNextButton,
      });

      renderExtraUi();
      bindEvents();
   }

   function resetInput() {
      if (!elements?.inputEl) {
         return;
      }

      elements.inputEl.value = '';
   }

   function mountRoot() {
      if (!mountEl || !elements?.rootEl) {
         return;
      }

      mountEl.replaceChildren(elements.rootEl);
   }

   function show() {
      if (!mountEl) {
         return;
      }

      ensureBuilt();
      selectionState.reload();
      mountRoot();
      resetInput();
      void searchRunner.runCurrentQuery();
   }

   function hide() {
      if (!mountEl) {
         return;
      }

      mountEl.replaceChildren();
   }

   return {
      show,
      hide,
      getSelectionSnapshot,
   };
}
