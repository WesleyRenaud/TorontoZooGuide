import { RemovedItemsPopupContentBuilder } from './removedItemsPopupContentBuilder.js';
import { RemovedItemsPopupSectionSpecs } from './removedItemsPopupSectionSpecs.js';

export class RemovedItemsPopupContent {
   static buildRemovedItemsPopupSections({
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

      return RemovedItemsPopupSectionSpecs.getRemovedItemsPopupSectionSpecs({
         added,
         removed,
         unscheduled,
         reducedVisibility,
         improvedVisibility,
         adjustments,
      })
         .map((section) => RemovedItemsPopupContentBuilder.makeSection(
            section.title,
            section.subtitle,
            RemovedItemsPopupContentBuilder.buildSectionRows(
               section.items,
               section.rowBuilder,
               section.stepKey,
               onViewAlternatives,
               removePopupOnly,
               section.showViewAlternatives ?? true,
               RemovedItemsPopupSectionSpecs.resolveKeepOverride(section, keepOverrideHandlers)
            )
         ))
         .filter(Boolean);
   }
}
