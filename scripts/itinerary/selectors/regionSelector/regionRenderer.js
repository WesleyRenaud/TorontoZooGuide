import {
   isRegionFullySelected,
   shouldHideDuplicateSingleExhibit,
} from './regionSelection.js';

function escapeHtml(value = '') {
   return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');
}

function buildChoiceRow({
   label,
   isSelected,
   action,
   regionName,
   exhibitName = '',
}) {
   const safeLabel = escapeHtml(label);
   const safeRegionName = escapeHtml(regionName);
   const safeExhibitName = escapeHtml(exhibitName);

   return `
      <button
         type="button"
         class="itin-panel-item itin-region-choice-row"
         data-action="${action}"
         data-region="${safeRegionName}"
         ${exhibitName ? `data-exhibit="${safeExhibitName}"` : ''}
      >
         <div class="itin-panel-item-left">
            <div class="itin-panel-text">
               <div class="itin-panel-name">${safeLabel}</div>
            </div>
         </div>

         <div class="itin-add-btn ${isSelected ? 'is-added' : ''}">
            ${isSelected ? '−' : '+'}
         </div>
      </button>
   `;
}

export function buildRegionRows(region, selectedExhibitNames) {
   const exhibits = Array.isArray(region.exhibits) ? region.exhibits : [];
   const regionSelected = isRegionFullySelected(region, selectedExhibitNames);

   const rows = [
      buildChoiceRow({
         label: region.name,
         isSelected: regionSelected,
         action: 'toggle-region',
         regionName: region.name,
      }),
   ];

   if (!shouldHideDuplicateSingleExhibit(region)) {
      exhibits.forEach((exhibitName) => {
         rows.push(
            buildChoiceRow({
               label: exhibitName,
               isSelected: selectedExhibitNames.has(exhibitName),
               action: 'toggle-exhibit',
               regionName: region.name,
               exhibitName,
            })
         );
      });
   }

   return rows.join('');
}