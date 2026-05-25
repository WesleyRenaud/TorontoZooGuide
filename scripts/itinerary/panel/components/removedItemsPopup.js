import {
   buildRemovedItemsPopupSections,
   hasRemovedItemsPopupContent,
} from './removedItemsPopupContent.js';
import { createRemovedItemsPopupLayout } from './removedItemsPopupLayout.js';

export function showRemovedItemsPopup({
   mountEl,
   added = {},
   removed = {},
   reducedVisibility = {},
   improvedVisibility = {},
   isEmptyItinerary = false,
   onAccept,
   onDismiss,
   onViewAlternatives,
} = {}) {
   if (!mountEl) return;

   if (!hasRemovedItemsPopupContent({ added, removed, reducedVisibility, improvedVisibility })) {
      return;
   }

   const {
      root,
      overlay,
      content,
      closeBtn,
      okBtn,
   } = createRemovedItemsPopupLayout({ isEmptyItinerary });

   let isCleanedUp = false;

   function removePopupOnly() {
      if (isCleanedUp) return;
      isCleanedUp = true;
      root.remove();
   }

   function acceptAndClose() {
      removePopupOnly();
      onAccept?.();
   }

   function dismissAndClose() {
      removePopupOnly();
      onDismiss?.();
   }

   buildRemovedItemsPopupSections({
      added,
      removed,
      reducedVisibility,
      improvedVisibility,
      onViewAlternatives,
      removePopupOnly,
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
