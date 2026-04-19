import { searchItineraryItems } from '../../api/searchApi.js';
import { createSelectorSelectionState } from './base/selectionState.js';
import {
   createDefaultSelectorRowLeftRenderer,
   renderSelectorResults,
} from './base/resultRenderer.js';
import { buildSelectorShell } from './base/shell.js';

function debounce(fn, delay = 250) {
   let t = null;
   return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
   };
}

function defaultMigrate(arr) {
   return Array.isArray(arr) ? arr : [];
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
   buildSearchPayload = (query) => ({ query }),
   extractRows,

   getContext = null,

   getId,
   getTitle = () => '',
   getSubtitle = () => '',
   getImageSrc = () => null,
   getInfoLink = () => null,

   makeSelection = (row) => ({ id: getId(row) }),

   topTitle = 'Itinerary Builder',
   h1 = 'Add Items',
   subtitle = 'Search and add items to your plan.',
   emptyText = 'No results found.',

   renderRowLeft,
   renderExtraControls = null,

   onBeforeToggleAdd = null,
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

   let root = null;
   let inputEl = null;
   let resultsEl = null;
   let bodyEl = null;

   const selectionState = createSelectorSelectionState({
      storageKey,
      migrateSelected,
      getId,
      makeSelection,
   });

   const defaultRenderRowLeft = createDefaultSelectorRowLeftRenderer({
      getTitle,
      getSubtitle,
      getImageSrc,
      getInfoLink,
   });

   function render(rows) {
      renderSelectorResults({
         resultsEl,
         rows,
         emptyText,
         getId,
         isSelected: selectionState.isSelected,
         renderRowLeft: renderRowLeft || defaultRenderRowLeft,
         onToggle: selectionState.toggleRow,
         onBeforeToggleAdd,
      });
   }

   async function runSearch() {
      const query = (inputEl?.value ?? '').trim();

      try {
         const ctx =
            typeof getContext === 'function'
               ? await getContext()
               : {};

         const payload = {
            ...buildSearchPayload(query),
            ...ctx,
         };

         const response = await searchItineraryItems(searchEndpoint, payload);
         const rows = extractRows(response);
         render(rows);
      } catch {
         render([]);
      }
   }

   function build() {
      const shell = buildSelectorShell({
         topTitle,
         h1,
         subtitle,
         hideNextButton,
      });

      root = shell.root;
      bodyEl = shell.bodyEl;
      inputEl = shell.inputEl;
      resultsEl = shell.resultsEl;

      if (typeof renderExtraControls === 'function') {
         renderExtraControls({
            rootEl: root,
            bodyEl,
            inputEl,
            resultsEl,
            rerunSearch: runSearch,
         });
      }

      inputEl.addEventListener('input', debounce(runSearch, 250));

      shell.prevButton?.addEventListener('click', () => onPrev?.());
      shell.nextButton?.addEventListener('click', () => onNext?.(selectionState.getSelectedSnapshot()));
      shell.finishButton?.addEventListener('click', () => onFinish?.(selectionState.getSelectedSnapshot()));
      shell.closeButton?.addEventListener('click', () => onClose?.());
   }

   function show() {
      if (!mountEl) return;

      if (!root) {
         build();
      }

      selectionState.reload();

      mountEl.innerHTML = '';
      mountEl.appendChild(root);

      inputEl.value = '';
      runSearch();
   }

   function hide() {
      if (!mountEl) return;
      mountEl.innerHTML = '';
   }

   return {
      show,
      hide,
   };
}
