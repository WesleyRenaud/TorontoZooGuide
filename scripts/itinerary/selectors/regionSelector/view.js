import { buildRegionRows } from './regionRenderer.js';

export function renderRegionSelectionView(resultsEl, regions, selectedExhibitNames) {
   if (!resultsEl) {
      return;
   }

   if (!Array.isArray(regions) || regions.length === 0) {
      resultsEl.innerHTML = `
         <div class="itin-empty">No regions available right now.</div>
      `;
      return;
   }

   resultsEl.innerHTML = regions
      .map((region) => buildRegionRows(region, selectedExhibitNames))
      .join('');
}

export function bindRegionSelectionEvents(resultsEl, {
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
