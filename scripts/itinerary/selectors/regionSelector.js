import {
   getExhibitsByRegion,
} from '../../api/itinerarySelectorApi.js';
import { createRegionSelectorState } from './regionSelector/state.js';
import { buildRegionSelectorShell } from './regionSelector/shell.js';
import {
   bindRegionSelectionEvents,
   renderRegionSelectionView,
} from './regionSelector/view.js';

export function createItineraryRegionSelectorController({
   mountEl,
   onPrev,
   onNext,
   onFinish,
   onClose,
} = {}) {
   let root = null;
   let resultsEl = null;

   const state = createRegionSelectorState();

   function renderRegions() {
      renderRegionSelectionView(
         resultsEl,
         state.getRegions(),
         state.getSelectedExhibitNamesSet()
      );
   }

   async function loadRegions() {
      const fetchedRegions = await getExhibitsByRegion();
      state.setRegions(fetchedRegions);
   }

   function build() {
      const shell = buildRegionSelectorShell();

      root = shell.root;
      resultsEl = shell.resultsEl;

      bindRegionSelectionEvents(resultsEl, {
         onToggleRegion: (regionName) => {
            if (state.toggleRegion(regionName)) {
               renderRegions();
            }
         },
         onToggleExhibit: (regionName, exhibitName) => {
            if (state.toggleExhibit(regionName, exhibitName)) {
               renderRegions();
            }
         },
      });

      shell.closeButton?.addEventListener('click', () => {
         onClose?.();
      });

      shell.prevButton?.addEventListener('click', () => {
         onPrev?.();
      });

      shell.nextButton?.addEventListener('click', async () => {
         const animals = await state.buildUpdatedAnimalsFromSelection();
         onNext?.(animals);
      });

      shell.finishButton?.addEventListener('click', async () => {
         const animals = await state.buildUpdatedAnimalsFromSelection();
         onFinish?.(animals);
      });
   }

   async function show() {
      if (!mountEl) return;

      if (!root) {
         build();
      }

      await loadRegions();
      state.hydrateSelectionsFromStorage();
      renderRegions();

      mountEl.innerHTML = '';
      mountEl.appendChild(root);
   }

   function hide() {
      if (!mountEl) return;
      mountEl.innerHTML = '';
   }

   function getSelectedRegions() {
      return state.getSelectedRegions();
   }

   function getSelectedExhibits() {
      return state.getSelectedExhibits();
   }

   return {
      show,
      hide,
      getSelectedRegions,
      getSelectedExhibits,
   };
}
