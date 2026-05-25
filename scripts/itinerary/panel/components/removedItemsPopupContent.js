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

function buildSectionRows(
   items,
   rowBuilder,
   stepKey,
   onViewAlternatives,
   removePopupOnly,
   showViewAlternatives = true
) {
   return rowBuilder(items).map((row) => {
      if (!showViewAlternatives) {
         return row;
      }

      return addAlternativesButton(
         row,
         stepKey,
         onViewAlternatives,
         removePopupOnly
      );
   });
}

function getSectionSpecs({
   added,
   removed,
   reducedVisibility,
   improvedVisibility,
} = {}) {
   const safeAdded = added ?? {};
   const safeRemoved = removed ?? {};
   const safeReduced = reducedVisibility ?? {};
   const safeImproved = improvedVisibility ?? {};

   return [
      {
         items: safeAdded.animals ?? [],
         title: APP_STRINGS.itinerary.removedItems.animalsAddedTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.animalsAddedSubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
         showViewAlternatives: false,
      },
      {
         items: safeRemoved.animals ?? [],
         title: APP_STRINGS.itinerary.removedItems.animalsRemovedTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.animalsRemovedSubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
      },
      {
         items: safeReduced.animals ?? [],
         title: APP_STRINGS.itinerary.removedItems.reducedAnimalVisibilityTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.reducedAnimalVisibilitySubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
      },
      {
         items: safeImproved.animals ?? [],
         title: APP_STRINGS.itinerary.removedItems.improvedAnimalVisibilityTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.improvedAnimalVisibilitySubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
         showViewAlternatives: false,
      },
      {
         items: safeRemoved.attractions ?? [],
         title: APP_STRINGS.map.filter.attractions,
         subtitle: APP_STRINGS.itinerary.removedItems.attractionsSubtitle,
         rowBuilder: buildAttractionRows,
         stepKey: 'attractions',
      },
      {
         items: safeRemoved.guardiansTalks ?? [],
         title: APP_STRINGS.site.nav.meetTheGuardians,
         subtitle: APP_STRINGS.itinerary.removedItems.talksSubtitle,
         rowBuilder: buildGuardiansRows,
         stepKey: 'guardiansTalks',
      },
      {
         items: safeRemoved.wildEncounters ?? [],
         title: APP_STRINGS.site.nav.wildEncounters,
         subtitle: APP_STRINGS.itinerary.removedItems.wildEncountersSubtitle,
         rowBuilder: buildWildRows,
         stepKey: 'wildEncounters',
      },
   ];
}

export function hasRemovedItemsPopupContent({
   added,
   removed,
   reducedVisibility,
   improvedVisibility,
} = {}) {
   return getSectionSpecs({ added, removed, reducedVisibility, improvedVisibility })
      .some((section) => Array.isArray(section.items) && section.items.length > 0);
}

export function buildRemovedItemsPopupSections({
   added,
   removed,
   reducedVisibility,
   improvedVisibility,
   onViewAlternatives,
   removePopupOnly,
} = {}) {
   return getSectionSpecs({ added, removed, reducedVisibility, improvedVisibility })
      .map((section) => makeSection(
         section.title,
         section.subtitle,
         buildSectionRows(
            section.items,
            section.rowBuilder,
            section.stepKey,
            onViewAlternatives,
            removePopupOnly,
            section.showViewAlternatives ?? true
         )
      ))
      .filter(Boolean);
}
