import { ItineraryPanelRowsBuilder } from '../itineraryPanelRowsBuilder.js';
import { RemovedItemsPopupContentRowsBuilder } from './removedItemsPopupContentRowsBuilder.js';
import { ItemType } from '../../../shared/enums/itemType.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { SpeciesExhibitKey } from '../../speciesExhibitKey.js';
import { Strings } from '../../../strings.js';
import { ItemKey } from '../../wizard/diff/itemKey.js';

export class RemovedItemsPopupSectionBuilder {
   static getUnscheduledSectionSpecs(
      safeUnscheduled = {},
      strings = Strings
   ) {
      const sections = [];

      if (safeUnscheduled.animals?.length) {
         sections.push({
            items: safeUnscheduled.animals,
            title: strings.itinerary.dayPlanner.unscheduledTitle,
            subtitle: strings.itinerary.removedItems.unscheduledSubtitle,
            rowBuilder: ItineraryPanelRowsBuilder.buildAnimalRows,
            stepKey: ScheduleItemKind.ANIMAL.itemType,
            showViewAlternatives: false,
         });
      }

      if (safeUnscheduled.attractions?.length) {
         sections.push({
            items: safeUnscheduled.attractions,
            title: strings.map.filter.attractions,
            subtitle: strings.itinerary.removedItems.unscheduledSubtitle,
            rowBuilder: ItineraryPanelRowsBuilder.buildAttractionRows,
            stepKey: ScheduleItemKind.ATTRACTION.itemType,
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
   } = {}, strings = Strings) {
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
            rowBuilder: RemovedItemsPopupContentRowsBuilder.buildAdjustmentRows,
            stepKey: 'date',
            showViewAlternatives: false,
         },
         {
            items: safeAdded.animals ?? [],
            title: strings.itinerary.removedItems.animalsAddedTitle,
            subtitle: strings.itinerary.removedItems.animalsAddedSubtitle,
            rowBuilder: ItineraryPanelRowsBuilder.buildAnimalRows,
            stepKey: ScheduleItemKind.ANIMAL.itemType,
            showViewAlternatives: false,
         },
         ...RemovedItemsPopupSectionBuilder.getUnscheduledSectionSpecs(safeUnscheduled, strings),
         {
            items: safeRemoved.animals ?? [],
            title: strings.itinerary.removedItems.animalsRemovedTitle,
            subtitle: strings.itinerary.removedItems.animalsRemovedSubtitle,
            rowBuilder: ItineraryPanelRowsBuilder.buildAnimalRows,
            stepKey: ScheduleItemKind.ANIMAL.itemType,
            keepOverrideKey: ItemType.ANIMAL,
         },
         {
            items: safeReduced.animals ?? [],
            title: strings.itinerary.removedItems.reducedAnimalVisibilityTitle,
            subtitle: strings.itinerary.removedItems.reducedAnimalVisibilitySubtitle,
            rowBuilder: ItineraryPanelRowsBuilder.buildAnimalRows,
            stepKey: ScheduleItemKind.ANIMAL.itemType,
         },
         {
            items: safeImproved.animals ?? [],
            title: strings.itinerary.removedItems.improvedAnimalVisibilityTitle,
            subtitle: strings.itinerary.removedItems.improvedAnimalVisibilitySubtitle,
            rowBuilder: ItineraryPanelRowsBuilder.buildAnimalRows,
            stepKey: ScheduleItemKind.ANIMAL.itemType,
            showViewAlternatives: false,
         },
         {
            items: safeRemoved.attractions ?? [],
            title: strings.itinerary.removedItems.attractionsRemovedTitle,
            subtitle: strings.itinerary.removedItems.attractionsSubtitle,
            rowBuilder: ItineraryPanelRowsBuilder.buildAttractionRows,
            stepKey: ScheduleItemKind.ATTRACTION.itemType,
            keepOverrideKey: ItemType.ATTRACTION,
         },
         {
            items: safeRemoved.guardiansTalks ?? [],
            title: strings.itinerary.removedItems.talksRemovedTitle,
            subtitle: strings.itinerary.removedItems.talksSubtitle,
            rowBuilder: ItineraryPanelRowsBuilder.buildGuardiansRows,
            stepKey: 'guardiansTalks',
         },
         {
            items: safeRemoved.wildEncounters ?? [],
            title: strings.itinerary.removedItems.wildEncountersRemovedTitle,
            subtitle: strings.itinerary.removedItems.wildEncountersSubtitle,
            rowBuilder: ItineraryPanelRowsBuilder.buildWildRows,
            stepKey: 'wildEncounters',
         },
      ];
   }

   static hasRemovedItemsPopupContent(sectionInput = {}) {
      return RemovedItemsPopupSectionBuilder.getRemovedItemsPopupSectionSpecs(sectionInput)
         .some((section) => Array.isArray(section.items) && section.items.length > 0);
   }

   static resolveKeepOverride(section, {
      onToggleKeepAnimal,
      isKeepAnimalSelected,
      onToggleKeepAttraction,
      isKeepAttractionSelected,
   } = {}) {
      if (section.keepOverrideKey === ItemType.ANIMAL) {
         return {
            buildKey: SpeciesExhibitKey.buildSpeciesExhibitKey,
            onToggle: onToggleKeepAnimal,
            isSelected: isKeepAnimalSelected,
         };
      }

      if (section.keepOverrideKey === ItemType.ATTRACTION) {
         return {
            buildKey: (item) => ItemKey.buildItemKey(item, 'name'),
            onToggle: onToggleKeepAttraction,
            isSelected: isKeepAttractionSelected,
         };
      }

      return null;
   }
}
