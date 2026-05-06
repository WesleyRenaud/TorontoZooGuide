import { el } from '../dom.js';
import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from '../rows.js';
import { APP_STRINGS } from '../../../strings.js';

function addAlternativesButton(rowNode, stepKey, onViewAlternatives, removePopupOnly) {
   if (!rowNode) return null;

   rowNode.classList.add('itin-removed-row');

   const btn = el(
      'button',
      'itin-removed-alt-btn',
      APP_STRINGS.itinerary.removedItems.viewAlternatives
   );
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
         title: APP_STRINGS.itinerary.removedItems.animalsRemovedTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.animalsRemovedSubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
      },
      {
         items: reducedVisibility.animals ?? [],
         title: APP_STRINGS.itinerary.removedItems.reducedAnimalVisibilityTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.reducedAnimalVisibilitySubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
      },
      {
         items: improvedVisibility.animals ?? [],
         title: APP_STRINGS.itinerary.removedItems.improvedAnimalVisibilityTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.improvedAnimalVisibilitySubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
      },
      {
         items: removed.attractions ?? [],
         title: APP_STRINGS.map.filter.attractions,
         subtitle: APP_STRINGS.itinerary.removedItems.attractionsSubtitle,
         rowBuilder: buildAttractionRows,
         stepKey: 'attractions',
      },
      {
         items: removed.guardiansTalks ?? [],
         title: APP_STRINGS.site.nav.meetTheGuardians,
         subtitle: APP_STRINGS.itinerary.removedItems.talksSubtitle,
         rowBuilder: buildGuardiansRows,
         stepKey: 'guardiansTalks',
      },
      {
         items: removed.wildEncounters ?? [],
         title: APP_STRINGS.site.nav.wildEncounters,
         subtitle: APP_STRINGS.itinerary.removedItems.wildEncountersSubtitle,
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
