import { buildAdjustmentRows } from './removedItemsPopupContentRows.js';
import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from '../rows.js';
import { buildSpeciesExhibitKey } from '../../speciesExhibitKey.js';
import { APP_STRINGS } from '../../../strings.js';
import { buildItemKey } from '../../wizard/diff/itemKey.js';

export function getUnscheduledSectionSpecs(
   safeUnscheduled = {},
   strings = APP_STRINGS
) {
   const sections = [];

   if (safeUnscheduled.animals?.length) {
      sections.push({
         items: safeUnscheduled.animals,
         title: strings.itinerary.dayPlanner.unscheduledTitle,
         subtitle: strings.itinerary.removedItems.unscheduledSubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
         showViewAlternatives: false,
      });
   }

   if (safeUnscheduled.attractions?.length) {
      sections.push({
         items: safeUnscheduled.attractions,
         title: strings.map.filter.attractions,
         subtitle: strings.itinerary.removedItems.unscheduledSubtitle,
         rowBuilder: buildAttractionRows,
         stepKey: 'attractions',
         showViewAlternatives: false,
      });
   }

   if (safeUnscheduled.guardiansTalks?.length) {
      sections.push({
         items: safeUnscheduled.guardiansTalks,
         title: strings.site.nav.meetTheGuardians,
         subtitle: strings.itinerary.removedItems.unscheduledSubtitle,
         rowBuilder: buildGuardiansRows,
         stepKey: 'guardiansTalks',
         showViewAlternatives: false,
      });
   }

   if (safeUnscheduled.wildEncounters?.length) {
      sections.push({
         items: safeUnscheduled.wildEncounters,
         title: strings.site.nav.wildEncounters,
         subtitle: strings.itinerary.removedItems.unscheduledSubtitle,
         rowBuilder: buildWildRows,
         stepKey: 'wildEncounters',
         showViewAlternatives: false,
      });
   }

   return sections;
}

export function getRemovedItemsPopupSectionSpecs({
   added,
   removed,
   unscheduled,
   reducedVisibility,
   improvedVisibility,
   adjustments,
} = {}, strings = APP_STRINGS) {
   const safeAdded = added ?? {};
   const safeRemoved = removed ?? {};
   const safeUnscheduled = unscheduled ?? {};
   const safeReduced = reducedVisibility ?? {};
   const safeImproved = improvedVisibility ?? {};

   return [
      {
         items: adjustments ?? [],
         title: strings.itinerary.removedItems.itineraryTimesTitle,
         subtitle: strings.itinerary.removedItems.itineraryTimesSubtitle,
         rowBuilder: buildAdjustmentRows,
         stepKey: 'date',
         showViewAlternatives: false,
      },
      {
         items: safeAdded.animals ?? [],
         title: strings.itinerary.removedItems.animalsAddedTitle,
         subtitle: strings.itinerary.removedItems.animalsAddedSubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
         showViewAlternatives: false,
      },
      ...getUnscheduledSectionSpecs(safeUnscheduled, strings),
      {
         items: safeRemoved.animals ?? [],
         title: strings.itinerary.removedItems.animalsRemovedTitle,
         subtitle: strings.itinerary.removedItems.animalsRemovedSubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
         keepOverrideKey: 'animal',
      },
      {
         items: safeReduced.animals ?? [],
         title: strings.itinerary.removedItems.reducedAnimalVisibilityTitle,
         subtitle: strings.itinerary.removedItems.reducedAnimalVisibilitySubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
      },
      {
         items: safeImproved.animals ?? [],
         title: strings.itinerary.removedItems.improvedAnimalVisibilityTitle,
         subtitle: strings.itinerary.removedItems.improvedAnimalVisibilitySubtitle,
         rowBuilder: buildAnimalRows,
         stepKey: 'animals',
         showViewAlternatives: false,
      },
      {
         items: safeRemoved.attractions ?? [],
         title: strings.map.filter.attractions,
         subtitle: strings.itinerary.removedItems.attractionsSubtitle,
         rowBuilder: buildAttractionRows,
         stepKey: 'attractions',
         keepOverrideKey: 'attraction',
      },
      {
         items: safeRemoved.guardiansTalks ?? [],
         title: strings.site.nav.meetTheGuardians,
         subtitle: strings.itinerary.removedItems.talksSubtitle,
         rowBuilder: buildGuardiansRows,
         stepKey: 'guardiansTalks',
      },
      {
         items: safeRemoved.wildEncounters ?? [],
         title: strings.site.nav.wildEncounters,
         subtitle: strings.itinerary.removedItems.wildEncountersSubtitle,
         rowBuilder: buildWildRows,
         stepKey: 'wildEncounters',
      },
   ];
}

export function hasRemovedItemsPopupContent(sectionInput = {}) {
   return getRemovedItemsPopupSectionSpecs(sectionInput)
      .some((section) => Array.isArray(section.items) && section.items.length > 0);
}

export function resolveKeepOverride(section, {
   onToggleKeepAnimal,
   isKeepAnimalSelected,
   onToggleKeepAttraction,
   isKeepAttractionSelected,
} = {}) {
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
