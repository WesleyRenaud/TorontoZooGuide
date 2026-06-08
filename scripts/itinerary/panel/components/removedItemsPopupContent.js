import { el } from '../dom.js';
import { formatClockTime } from '../format.js';
import { makeItemRow } from './itemRow.js';
import { getItineraryAdjustmentTypes } from '../../itineraryAdjustmentTypes.js';
import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from '../rows.js';
import { buildSpeciesExhibitKey } from '../../speciesExhibitKey.js';
import { APP_STRINGS } from '../../../strings.js';
import { buildItemKey } from '../../wizard/diff/itemKey.js';

function addAlternativesButton(rowNode, stepKey, onViewAlternatives, removePopupOnly) {
   if (!rowNode) return null;
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

   return btn;
}

function addKeepOverrideButton(
      item,
      buildKey,
      onToggleKeep,
      isKeepSelected) {
   if (!item) return null;

   const key = buildKey(item);

   if (!key) {
      return null;
   }

   const btn = el('button', 'itin-removed-alt-btn itin-removed-keep-btn');
   btn.type = 'button';

   function sync() {
      const selected = Boolean(isKeepSelected?.(key));
      const removedItemsStrings = APP_STRINGS.itinerary.removedItems;

      btn.classList.toggle('is-selected', selected);
      btn.setAttribute('aria-pressed', selected ? 'true' : 'false');
      btn.textContent = selected
         ? APP_STRINGS.itinerary.dayPlanner.remove
         : removedItemsStrings.keepInItinerary;
      btn.title = selected ? removedItemsStrings.removeFromItineraryHint : '';
   }

   btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      onToggleKeep?.(item);
      sync();
   });

   sync();
   return btn;
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

function buildAdjustmentRow(adjustment = {}) {
   const adjustmentTypes = getItineraryAdjustmentTypes();
   const oldTime = formatClockTime(adjustment.previousValue);
   const newTime = formatClockTime(adjustment.value);

   if (!oldTime || !newTime) {
      return null;
   }

   if (adjustment.type === adjustmentTypes?.ARRIVAL_TIME_ADJUSTED) {
      return makeItemRow({
         name: APP_STRINGS.itinerary.dayPlanner.arrivalLabel,
         alertLine: APP_STRINGS.itinerary.removedItems.arrivalAdjusted(oldTime, newTime),
      });
   }

   if (adjustment.type === adjustmentTypes?.DEPARTURE_TIME_ADJUSTED) {
      return makeItemRow({
         name: APP_STRINGS.labels.departure,
         alertLine: APP_STRINGS.itinerary.removedItems.departureAdjusted(oldTime, newTime),
      });
   }

   return null;
}

function buildAdjustmentRows(adjustments = []) {
   return adjustments.map((adjustment) => buildAdjustmentRow(adjustment));
}

function hasUnscheduledItems(unscheduled = {}) {
   return Boolean(
      unscheduled?.animals?.length || unscheduled?.attractions?.length
   );
}

function buildUnscheduledRows(unscheduledGroups = []) {
   const unscheduled = unscheduledGroups[0] ?? {};

   return [
      ...buildAnimalRows(unscheduled.animals ?? []),
      ...buildAttractionRows(unscheduled.attractions ?? []),
   ];
}

function buildSectionRows(
   items,
   rowBuilder,
   stepKey,
   onViewAlternatives,
   removePopupOnly,
   showViewAlternatives = true,
   keepOverride = null
) {
   return rowBuilder(items).map((row, index) => {
      const item = items?.[index];

      if (!showViewAlternatives && !keepOverride) {
         return row;
      }

      row.classList.add('itin-removed-row');

      const actions = el('div', 'itin-removed-row-actions');

      if (showViewAlternatives) {
         const alternativesButton = addAlternativesButton(
            row,
            stepKey,
            onViewAlternatives,
            removePopupOnly
         );

         if (alternativesButton) {
            actions.appendChild(alternativesButton);
         }
      }

      if (keepOverride) {
         const keepButton = addKeepOverrideButton(
            item,
            keepOverride.buildKey,
            keepOverride.onToggle,
            keepOverride.isSelected
         );

         if (keepButton) {
            actions.appendChild(keepButton);
         }
      }

      if (actions.childElementCount > 0) {
         row.appendChild(actions);
      }

      return row;
   });
}

function getSectionSpecs({
   added,
   removed,
   unscheduled,
   reducedVisibility,
   improvedVisibility,
   adjustments,
} = {}) {
   const safeAdded = added ?? {};
   const safeRemoved = removed ?? {};
   const safeUnscheduled = unscheduled ?? {};
   const safeReduced = reducedVisibility ?? {};
   const safeImproved = improvedVisibility ?? {};

   return [
      {
         items: adjustments ?? [],
         title: APP_STRINGS.itinerary.removedItems.itineraryTimesTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.itineraryTimesSubtitle,
         rowBuilder: buildAdjustmentRows,
         stepKey: 'date',
         showViewAlternatives: false,
      },
      {
         items: safeAdded.animals ?? [],
         title: APP_STRINGS.itinerary.removedItems.animalsAddedTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.animalsAddedSubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
         showViewAlternatives: false,
      },
      {
         items: hasUnscheduledItems(safeUnscheduled) ? [safeUnscheduled] : [],
         title: APP_STRINGS.itinerary.dayPlanner.unscheduledTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.unscheduledSubtitle,
         rowBuilder: buildUnscheduledRows,
         stepKey: 'date',
         showViewAlternatives: false,
      },
      {
         items: safeRemoved.animals ?? [],
         title: APP_STRINGS.itinerary.removedItems.animalsRemovedTitle,
         subtitle: APP_STRINGS.itinerary.removedItems.animalsRemovedSubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
         keepOverrideKey: 'animal',
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
         keepOverrideKey: 'attraction',
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
   unscheduled,
   reducedVisibility,
   improvedVisibility,
   adjustments,
} = {}) {
   return getSectionSpecs({
      added,
      removed,
      unscheduled,
      reducedVisibility,
      improvedVisibility,
      adjustments,
   })
      .some((section) => Array.isArray(section.items) && section.items.length > 0);
}

function resolveKeepOverride(section, {
   onToggleKeepAnimal,
   isKeepAnimalSelected,
   onToggleKeepAttraction,
   isKeepAttractionSelected,
}) {
   if (section.keepOverrideKey === 'animal') {
      return {
         buildKey: buildSpeciesExhibitKey,
         onToggle: onToggleKeepAnimal,
         isSelected: isKeepAnimalSelected,
      };
   }

   if (section.keepOverrideKey === 'attraction') {
      return {
         buildKey: (item) => buildItemKey(item, 'name'),
         onToggle: onToggleKeepAttraction,
         isSelected: isKeepAttractionSelected,
      };
   }

   return null;
}

export function buildRemovedItemsPopupSections({
   added,
   removed,
   unscheduled,
   reducedVisibility,
   improvedVisibility,
   adjustments,
   onViewAlternatives,
   removePopupOnly,
   onToggleKeepAnimal,
   isKeepAnimalSelected,
   onToggleKeepAttraction,
   isKeepAttractionSelected,
} = {}) {
   const keepOverrideHandlers = {
      onToggleKeepAnimal,
      isKeepAnimalSelected,
      onToggleKeepAttraction,
      isKeepAttractionSelected,
   };

   return getSectionSpecs({
      added,
      removed,
      unscheduled,
      reducedVisibility,
      improvedVisibility,
      adjustments,
   })
      .map((section) => makeSection(
         section.title,
         section.subtitle,
         buildSectionRows(
            section.items,
            section.rowBuilder,
            section.stepKey,
            onViewAlternatives,
            removePopupOnly,
            section.showViewAlternatives ?? true,
            resolveKeepOverride(section, keepOverrideHandlers)
         )
      ))
      .filter(Boolean);
}
