import { RemovedItemsPopupContent } from './removedItemsPopupContent.js';
import { RemovedItemsPopupLayout } from './removedItemsPopupLayout.js';
import { RemovedItemsPopupSectionSpecs } from './removedItemsPopupSectionSpecs.js';
import { SpeciesExhibitKey } from '../../speciesExhibitKey.js';
import { ItemKey } from '../../wizard/diff/itemKey.js';

function toggleKeptItem(keptItemsByKey, item, buildKey, normalizeItem) {
   const key = buildKey(item);

   if (!key) {
      return;
   }

   if (keptItemsByKey.has(key)) {
      keptItemsByKey.delete(key);
      return;
   }

   keptItemsByKey.set(key, normalizeItem(item));
}

export class RemovedItemsPopup {
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

      if (!RemovedItemsPopupSectionSpecs.hasRemovedItemsPopupContent({
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
      } = RemovedItemsPopupLayout.createRemovedItemsPopupLayout({ isEmptyItinerary });
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

      RemovedItemsPopupContent.buildRemovedItemsPopupSections({
         added,
         removed,
         unscheduled,
         reducedVisibility,
         improvedVisibility,
         adjustments,
         onViewAlternatives,
         removePopupOnly,
         onToggleKeepAnimal: (animal) => {
            toggleKeptItem(
               keptAnimalsByKey,
               animal,
               SpeciesExhibitKey.buildSpeciesExhibitKey,
               (value) => ({
                  species: String(value?.species ?? '').trim(),
                  exhibit: String(value?.exhibit ?? '').trim(),
               })
            );
         },
         isKeepAnimalSelected: (key) => keptAnimalsByKey.has(key),
         onToggleKeepAttraction: (attraction) => {
            toggleKeptItem(
               keptAttractionsByKey,
               attraction,
               (value) => ItemKey.buildItemKey(value, 'name'),
               (value) => String(value?.name ?? '').trim()
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
