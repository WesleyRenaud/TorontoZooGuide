import { ItinerarySelectorClient } from '../../api/itinerarySelectorClient.js';
import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { DraftStore } from '../draftStore.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { RegionSelectorRenderer } from './regionSelector/regionSelectorRenderer.js';
import { RegionSelectorStore } from './regionSelector/regionSelectorStore.js';
import { RegionStore } from './regionSelector/regionStore.js';
import { RegionSelectorView } from './regionSelectorView.js';
import { StorageKeys } from '../storageKeys.js';

export class RegionSelector {
   static shouldSkipRegionSelectionSync({
   fingerprintAtShow = '',
   fingerprintNow = '',
   selectionChangedSinceShow: selectionChanged = false,
} = {}) {
      if (selectionChanged) {
         return false;
      }

      return fingerprintAtShow === fingerprintNow;
   }

   static createItineraryRegionSelectorController({
   mountEl,
   onPrev,
   onNext,
   onFinish,
   onClose,
} = {}) {
      let elements = null;
      const state = RegionSelectorStore.createRegionSelectorState();
      let exhibitFingerprintAtShow = '';
      let selectionChangedSinceShow = false;

      function buildExhibitSelectionFingerprint() {
         return [...state.getSelectedExhibitNamesSet()]
            .map(ValueNormalizer.asTrimmedString)
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

         RegionSelectorRenderer.renderRegionSelectionView(
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
         RegionSelectorRenderer.bindRegionSelectionEvents(elements?.resultsEl, {
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

         elements = RegionSelectorView.createRegionSelectorElements();
         bindEvents();
      }

      async function refreshRegions() {
         const context = await ItinerarySearchContext.getItineraryDateSearchContext({ includeTemp: false });
         state.setRegions(await ItinerarySelectorClient.getExhibitsByRegion(context));
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

         if (RegionStore.selectedExhibitsNeedAnimalRebuild(
            state.getSelectedExhibitNamesSet(),
            DraftStore.loadArray(StorageKeys.ANIMALS_KEY)
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
}
