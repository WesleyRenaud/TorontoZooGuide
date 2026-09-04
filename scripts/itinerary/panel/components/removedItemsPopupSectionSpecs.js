import { RemovedItemsPopupContentRows } from './removedItemsPopupContentRows.js';
import { Rows } from '../rows.js';
import { SpeciesExhibitKey } from '../../speciesExhibitKey.js';
import { APP_STRINGS } from '../../../strings.js';
import { ItemKey } from '../../wizard/diff/itemKey.js';

export class RemovedItemsPopupSectionSpecs {
   static getUnscheduledSectionSpecs(
      safeUnscheduled = {},
      strings = APP_STRINGS
   ) {
      const sections = [];

      if (safeUnscheduled.animals?.length) {
         sections.push({
            items: safeUnscheduled.animals,
            title: strings.itinerary.dayPlanner.unscheduledTitle,
            subtitle: strings.itinerary.removedItems.unscheduledSubtitle,
            rowBuilder: Rows.buildAnimalRows,
            stepKey: 'animals',
            showViewAlternatives: false,
         });
      }

      if (safeUnscheduled.attractions?.length) {
         sections.push({
            items: safeUnscheduled.attractions,
            title: strings.map.filter.attractions,
            subtitle: strings.itinerary.removedItems.unscheduledSubtitle,
            rowBuilder: Rows.buildAttractionRows,
            stepKey: 'attractions',
            showViewAlternatives: false,
         });
      }

      return sections;
   }

   static getRemovedItemsPopupSectionSpecs({
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
            rowBuilder: RemovedItemsPopupContentRows.buildAdjustmentRows,
            stepKey: 'date',
            showViewAlternatives: false,
         },
         {
            items: safeAdded.animals ?? [],
            title: strings.itinerary.removedItems.animalsAddedTitle,
            subtitle: strings.itinerary.removedItems.animalsAddedSubtitle,
            rowBuilder: Rows.buildAnimalRows,
            stepKey: 'animals',
            showViewAlternatives: false,
         },
         ...RemovedItemsPopupSectionSpecs.getUnscheduledSectionSpecs(safeUnscheduled, strings),
         {
            items: safeRemoved.animals ?? [],
            title: strings.itinerary.removedItems.animalsRemovedTitle,
            subtitle: strings.itinerary.removedItems.animalsRemovedSubtitle,
            rowBuilder: Rows.buildAnimalRows,
            stepKey: 'animals',
            keepOverrideKey: 'animal',
         },
         {
            items: safeReduced.animals ?? [],
            title: strings.itinerary.removedItems.reducedAnimalVisibilityTitle,
            subtitle: strings.itinerary.removedItems.reducedAnimalVisibilitySubtitle,
            rowBuilder: Rows.buildAnimalRows,
            stepKey: 'animals',
         },
         {
            items: safeImproved.animals ?? [],
            title: strings.itinerary.removedItems.improvedAnimalVisibilityTitle,
            subtitle: strings.itinerary.removedItems.improvedAnimalVisibilitySubtitle,
            rowBuilder: Rows.buildAnimalRows,
            stepKey: 'animals',
            showViewAlternatives: false,
         },
         {
            items: safeRemoved.attractions ?? [],
            title: strings.map.filter.attractions,
            subtitle: strings.itinerary.removedItems.attractionsSubtitle,
            rowBuilder: Rows.buildAttractionRows,
            stepKey: 'attractions',
            keepOverrideKey: 'attraction',
         },
         {
            items: safeRemoved.guardiansTalks ?? [],
            title: strings.site.nav.meetTheGuardians,
            subtitle: strings.itinerary.removedItems.talksSubtitle,
            rowBuilder: Rows.buildGuardiansRows,
            stepKey: 'guardiansTalks',
         },
         {
            items: safeRemoved.wildEncounters ?? [],
            title: strings.site.nav.wildEncounters,
            subtitle: strings.itinerary.removedItems.wildEncountersSubtitle,
            rowBuilder: Rows.buildWildRows,
            stepKey: 'wildEncounters',
         },
      ];
   }

   static hasRemovedItemsPopupContent(sectionInput = {}) {
      return RemovedItemsPopupSectionSpecs.getRemovedItemsPopupSectionSpecs(sectionInput)
         .some((section) => Array.isArray(section.items) && section.items.length > 0);
   }

   static resolveKeepOverride(section, {
      onToggleKeepAnimal,
      isKeepAnimalSelected,
      onToggleKeepAttraction,
      isKeepAttractionSelected,
   } = {}) {
      if (section.keepOverrideKey === 'animal') {
         return {
            buildKey: SpeciesExhibitKey.buildSpeciesExhibitKey,
            onToggle: onToggleKeepAnimal,
            isSelected: isKeepAnimalSelected,
         };
      }

      if (section.keepOverrideKey === 'attraction') {
         return {
            buildKey: (item) => ItemKey.buildItemKey(item, 'name'),
            onToggle: onToggleKeepAttraction,
            isSelected: isKeepAttractionSelected,
         };
      }

      return null;
   }
}
