import { el } from '../dom.js';
import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from '../rows.js';

function addAlternativesButton(rowNode, stepKey, onViewAlternatives, removePopupOnly) {
   if (!rowNode) return null;

   rowNode.classList.add('itin-removed-row');

   const btn = el('button', 'itin-removed-alt-btn', 'View Alternatives');
   btn.type = 'button';

   btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      removePopupOnly();
      onViewAlternatives?.(stepKey);
   });

   rowNode.appendChild(btn);
   return rowNode;
}

function makeSection(title, subtitle, rowNodes = []) {
   const validRows = rowNodes.filter(Boolean);
   if (!validRows.length) return null;

   const section = el('div', 'itin-removed-section');

   section.appendChild(
      el('div', 'itin-removed-section-title', title)
   );

   if (subtitle) {
      section.appendChild(
         el('div', 'itin-removed-section-subtitle', subtitle)
      );
   }

   const list = el('div', 'itin-removed-list');

   validRows.forEach((node) => {
      list.appendChild(node);
   });

   section.appendChild(list);
   return section;
}

function buildSectionRows(items, rowBuilder, stepKey, onViewAlternatives, removePopupOnly) {
   return rowBuilder(items).map((row) =>
      addAlternativesButton(row, stepKey, onViewAlternatives, removePopupOnly)
   );
}

function getSectionSpecs({
   removed = {},
   reducedVisibility = {},
   improvedVisibility = {},
} = {}) {
   return [
      {
         items: removed.animals ?? [],
         title: 'Animals Removed',
         subtitle: 'The following animals are unavailable on your new date for the reasons listed below.',
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
      },
      {
         items: reducedVisibility.animals ?? [],
         title: 'Reduced Animal Visibility',
         subtitle: 'The following animals remain on your itinerary, but are expected to be less visible on your new date.',
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
      },
      {
         items: improvedVisibility.animals ?? [],
         title: 'Improved Animal Visibility',
         subtitle: 'The following animals remain on your itinerary and are expected to be easier to see on your new date.',
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
      },
      {
         items: removed.attractions ?? [],
         title: 'Attractions',
         subtitle: 'The following attractions are unavailable on your new date.',
         rowBuilder: buildAttractionRows,
         stepKey: 'attractions',
      },
      {
         items: removed.guardiansTalks ?? [],
         title: 'Meet the Guardians',
         subtitle: 'The following talks are not scheduled on your new date.',
         rowBuilder: buildGuardiansRows,
         stepKey: 'guardiansTalks',
      },
      {
         items: removed.wildEncounters ?? [],
         title: 'Wild Encounters',
         subtitle: 'The following encounters are not available on your new date.',
         rowBuilder: buildWildRows,
         stepKey: 'wildEncounters',
      },
   ];
}

export function hasRemovedItemsPopupContent({
   removed = {},
   reducedVisibility = {},
   improvedVisibility = {},
} = {}) {
   return getSectionSpecs({ removed, reducedVisibility, improvedVisibility })
      .some((section) => Array.isArray(section.items) && section.items.length > 0);
}

export function buildRemovedItemsPopupSections({
   removed = {},
   reducedVisibility = {},
   improvedVisibility = {},
   onViewAlternatives,
   removePopupOnly,
} = {}) {
   return getSectionSpecs({ removed, reducedVisibility, improvedVisibility })
      .map((section) => makeSection(
         section.title,
         section.subtitle,
         buildSectionRows(
            section.items,
            section.rowBuilder,
            section.stepKey,
            onViewAlternatives,
            removePopupOnly
         )
      ))
      .filter(Boolean);
}
