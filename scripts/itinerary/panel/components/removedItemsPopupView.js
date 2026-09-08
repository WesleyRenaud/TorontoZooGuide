import { RemovedItemsPopupContentBuilder } from './removedItemsPopupContentBuilder.js';
import { RemovedItemsPopupSectionBuilder } from './removedItemsPopupSectionBuilder.js';

export class RemovedItemsPopupView {
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

      return RemovedItemsPopupSectionBuilder.getRemovedItemsPopupSectionSpecs({
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
               RemovedItemsPopupSectionBuilder.resolveKeepOverride(section, keepOverrideHandlers)
            )
         ))
         .filter(Boolean);
   }
}
