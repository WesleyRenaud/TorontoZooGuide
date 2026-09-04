import { ItinerarySelectorApi } from '../../api/itinerarySelectorApi.js';
import { loadArray } from '../draftStorage.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { RegionSelection } from './regionSelector/regionSelection.js';
import { buildRegionSelectorShell } from './regionSelector/shell.js';
import { createRegionSelectorState } from './regionSelector/state.js';
import {
   bindRegionSelectionEvents,
   renderRegionSelectionView,
} from './regionSelector/view.js';
import { StorageKeys } from '../storageKeys.js';

export function shouldSkipRegionSelectionSync({
   fingerprintAtShow = '',
   fingerprintNow = '',
   selectionChangedSinceShow: selectionChanged = false,
} = {}) {
   if (selectionChanged) {
      return false;
   }

   return fingerprintAtShow === fingerprintNow;
}

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
   let selectionChangedSinceShow = false;

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

   function markSelectionChanged() {
      selectionChangedSinceShow = true;
   }

   function handleRegionToggle(regionName) {
      const changed = state.toggleRegion(regionName);

      if (changed) {
         markSelectionChanged();
      }

      rerenderIfChanged(changed);
   }

   function handleExhibitToggle(regionName, exhibitName) {
      const changed = state.toggleExhibit(regionName, exhibitName);

      if (changed) {
         markSelectionChanged();
      }

      rerenderIfChanged(changed);
   }

   async function commitSelection(callback) {
      const animals = await getSelectionSnapshot();

      selectionChangedSinceShow = false;
      exhibitFingerprintAtShow = buildExhibitSelectionFingerprint();
      callback?.(animals);
   }

   function bindEvents() {
      bindRegionSelectionEvents(elements?.resultsEl, {
         onToggleRegion: handleRegionToggle,
         onToggleExhibit: handleExhibitToggle,
      });

      elements?.closeButtonEl?.addEventListener('click', () => {
         onClose?.();
      });

      elements?.prevButtonEl?.addEventListener('click', async () => {
         if (shouldSkipClosingSelectionSync()) {
            onPrev?.(null);
            return;
         }

         await commitSelection(onPrev);
      });

      elements?.nextButtonEl?.addEventListener('click', async () => {
         if (shouldSkipClosingSelectionSync()) {
            onNext?.(null);
            return;
         }

         await commitSelection(onNext);
      });

      elements?.finishButtonEl?.addEventListener('click', async () => {
         if (shouldSkipClosingSelectionSync()) {
            onFinish?.(null);
            return;
         }

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
      const context = await ItinerarySearchContext.getItineraryDateSearchContext({ includeTemp: false });
      state.setRegions(await ItinerarySelectorApi.getExhibitsByRegion(context));
      await state.hydrateSelectionsFromStorage();
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
      selectionChangedSinceShow = false;
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
      if (selectionChangedSinceShow) {
         return false;
      }

      if (state.selectedExhibitsNeedCatalogRebuild()) {
         return false;
      }

      if (RegionSelection.selectedExhibitsNeedAnimalRebuild(
         state.getSelectedExhibitNamesSet(),
         loadArray(StorageKeys.ANIMALS_KEY)
      )) {
         return false;
      }

      return buildExhibitSelectionFingerprint() === exhibitFingerprintAtShow;
   }

   return {
      show,
      hide,
      getSelectionSnapshot,
      shouldSkipClosingSelectionSync,
   };
}
