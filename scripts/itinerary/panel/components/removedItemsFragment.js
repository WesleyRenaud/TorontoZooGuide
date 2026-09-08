import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { RemovedItemsPopupHelper } from './removedItemsPopupHelper.js';
import { RemovedItemsPopupLayoutView } from './removedItemsPopupLayoutView.js';
import { RemovedItemsPopupSectionBuilder } from './removedItemsPopupSectionBuilder.js';
import { RemovedItemsPopupView } from './removedItemsPopupView.js';
import { SpeciesExhibitKey } from '../../speciesExhibitKey.js';
import { ItemKey } from '../../wizard/diff/itemKey.js';

export class RemovedItemsFragment {
   static showRemovedItemsPopup({
      mountEl,
      added = {},
      removed = {},
      unscheduled = {},
      reducedVisibility = {},
      improvedVisibility = {},
      adjustments = [],
      isEmptyItinerary = false,
      onAccept,
      onDismiss,
      onViewAlternatives,
   } = {}) {
      if (!mountEl) return;

      if (!RemovedItemsPopupSectionBuilder.hasRemovedItemsPopupContent({
         added,
         removed,
         unscheduled,
         reducedVisibility,
         improvedVisibility,
         adjustments,
      })) {
         return;
      }

      const {
         root,
         overlay,
         content,
         closeBtn,
         okBtn,
      } = RemovedItemsPopupLayoutView.createRemovedItemsPopupLayout({ isEmptyItinerary });
      const keptAnimalsByKey = new Map();
      const keptAttractionsByKey = new Map();

      let isCleanedUp = false;

      function removePopupOnly() {
         if (isCleanedUp) return;
         isCleanedUp = true;
         root.remove();
      }

      function acceptAndClose() {
         removePopupOnly();
         onAccept?.({
            animalsToKeep: Array.from(keptAnimalsByKey.values()),
            attractionsToKeep: Array.from(keptAttractionsByKey.values()),
         });
      }

      function dismissAndClose() {
         removePopupOnly();
         onDismiss?.();
      }

      RemovedItemsPopupView.buildRemovedItemsPopupSections({
         added,
         removed,
         unscheduled,
         reducedVisibility,
         improvedVisibility,
         adjustments,
         onViewAlternatives,
         removePopupOnly,
         onToggleKeepAnimal: (animal) => {
            RemovedItemsPopupHelper.toggleKeptItem(
               keptAnimalsByKey,
               animal,
               SpeciesExhibitKey.buildSpeciesExhibitKey,
               (value) => ({
                  species: ValueNormalizer.asTrimmedString(value?.species),
                  exhibit: ValueNormalizer.asTrimmedString(value?.exhibit),
               })
            );
         },
         isKeepAnimalSelected: (key) => keptAnimalsByKey.has(key),
         onToggleKeepAttraction: (attraction) => {
            RemovedItemsPopupHelper.toggleKeptItem(
               keptAttractionsByKey,
               attraction,
               (value) => ItemKey.buildItemKey(value, 'name'),
               (value) => ValueNormalizer.asTrimmedString(value?.name)
            );
         },
         isKeepAttractionSelected: (key) => keptAttractionsByKey.has(key),
      }).forEach((section) => content.appendChild(section));

      closeBtn.addEventListener('click', dismissAndClose);
      okBtn.addEventListener('click', acceptAndClose);

      overlay.addEventListener('click', (e) => {
         if (e.target === overlay) {
            dismissAndClose();
         }
      });

      mountEl.appendChild(root);
   }
}
