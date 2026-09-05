import { RegionRenderer } from './regionRenderer.js';
import { APP_STRINGS } from '../../../strings.js';

function createEmptyState(message) {
   const emptyEl = document.createElement('div');
   emptyEl.className = 'itin-empty';
   emptyEl.textContent = message;
   return emptyEl;
}

export class View {
   static renderRegionSelectionView(resultsEl, regions, selectedExhibitNames) {
      if (!resultsEl) {
         return;
      }

      if (regions.length === 0) {
         resultsEl.replaceChildren(
            createEmptyState(APP_STRINGS.itinerary.emptyText.regions)
         );
         return;
      }

      const fragment = document.createDocumentFragment();

      regions.forEach((region) => {
         RegionRenderer.buildRegionRows(region, selectedExhibitNames).forEach((row) => {
            fragment.appendChild(row);
         });
      });

      resultsEl.replaceChildren(fragment);

   }

   static bindRegionSelectionEvents(resultsEl, {
      onToggleRegion,
      onToggleExhibit,
   } = {}) {
      if (!resultsEl) {
         return;
      }

      resultsEl.addEventListener('click', (event) => {
         const button = event.target.closest('[data-action]');

         if (!button || !resultsEl.contains(button)) {
            return;
         }

         const action = button.dataset.action;
         const regionName = button.dataset.region || '';
         const exhibitName = button.dataset.exhibit || '';

         if (action === 'toggle-region') {
            onToggleRegion?.(regionName);
            return;
         }

         if (action === 'toggle-exhibit') {
            onToggleExhibit?.(regionName, exhibitName);
         }
      });
   }
}
