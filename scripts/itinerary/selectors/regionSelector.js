import { getExhibitsByRegion } from '../../api/itinerarySelectorApi.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { buildRegionSelectorShell } from './regionSelector/shell.js';
import { createRegionSelectorState } from './regionSelector/state.js';
import {
   bindRegionSelectionEvents,
   renderRegionSelectionView,
} from './regionSelector/view.js';

function createRegionSelectorElements() {
   const shell = buildRegionSelectorShell();

   return {
      rootEl: shell.root,
      resultsEl: shell.resultsEl,
      prevButtonEl: shell.prevButton,
      nextButtonEl: shell.nextButton,
      finishButtonEl: shell.finishButton,
      closeButtonEl: shell.closeButton,
   };
}

export function createItineraryRegionSelectorController({
   mountEl,
   onPrev,
   onNext,
   onFinish,
   onClose,
} = {}) {
   let elements = null;
   const state = createRegionSelectorState();
   let exhibitFingerprintAtShow = '';

   function buildExhibitSelectionFingerprint() {
      return [...state.getSelectedExhibitNamesSet()]
         .map((name) => String(name).trim())
         .filter(Boolean)
         .sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }))
         .join('\0');
   }

   function getSelectionSnapshot() {
      return state.buildUpdatedAnimalsFromSelection();
   }

   function renderRegions() {
      if (!elements?.resultsEl) {
         return;
      }

      renderRegionSelectionView(
         elements.resultsEl,
         state.getRegions(),
         state.getSelectedExhibitNamesSet()
      );
   }

   function rerenderIfChanged(changed) {
      if (!changed) {
         return;
      }

      renderRegions();
   }

   function handleRegionToggle(regionName) {
      rerenderIfChanged(state.toggleRegion(regionName));
   }

   function handleExhibitToggle(regionName, exhibitName) {
      rerenderIfChanged(state.toggleExhibit(regionName, exhibitName));
   }

   async function commitSelection(callback) {
      callback?.(await getSelectionSnapshot());
   }

   function bindEvents() {
      bindRegionSelectionEvents(elements?.resultsEl, {
         onToggleRegion: handleRegionToggle,
         onToggleExhibit: handleExhibitToggle,
      });

      elements?.closeButtonEl?.addEventListener('click', () => {
         onClose?.();
      });

      elements?.prevButtonEl?.addEventListener('click', () => {
         onPrev?.();
      });

      elements?.nextButtonEl?.addEventListener('click', async () => {
         await commitSelection(onNext);
      });

      elements?.finishButtonEl?.addEventListener('click', async () => {
         await commitSelection(onFinish);
      });
   }

   function ensureBuilt() {
      if (elements) {
         return;
      }

      elements = createRegionSelectorElements();
      bindEvents();
   }

   async function refreshRegions() {
      const context = await getItineraryDateSearchContext({ includeTemp: false });
      state.setRegions(await getExhibitsByRegion(context));
      state.hydrateSelectionsFromStorage();
      renderRegions();
   }

   function mountRoot() {
      if (!mountEl || !elements?.rootEl) {
         return;
      }

      mountEl.replaceChildren(elements.rootEl);
   }

   async function show() {
      if (!mountEl) {
         return;
      }

      ensureBuilt();
      await refreshRegions();
      exhibitFingerprintAtShow = buildExhibitSelectionFingerprint();
      mountRoot();
   }

   function hide() {
      if (!mountEl) {
         return;
      }

      mountEl.replaceChildren();
   }

   function shouldSkipClosingSelectionSync() {
      return buildExhibitSelectionFingerprint() === exhibitFingerprintAtShow;
   }

   return {
      show,
      hide,
      getSelectionSnapshot,
      shouldSkipClosingSelectionSync,
   };
}
