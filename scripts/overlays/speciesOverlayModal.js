import { OverlayModal } from './overlayModal.js';

export class SpeciesOverlayModal {
   static TITLE_ID = 'speciesOverlayTitle';
   static POINTER_OPENED_ATTRIBUTE = OverlayModal.POINTER_OPENED_ATTRIBUTE;
   static NON_CONTENT_TAGS = OverlayModal.NON_CONTENT_TAGS;

   static createSpeciesOverlayModal({ getOverlay, getDialog }) {
      return OverlayModal.createOverlayModal({
         getOverlay,
         getDialog,
         getTitle: SpeciesOverlayModal.getSpeciesTitle,
         titleId: SpeciesOverlayModal.TITLE_ID,
         decorateDialog: SpeciesOverlayModal.decorateSpeciesDialog,
      });
   }

   static getSpeciesTitle(dialog) {
      return dialog?.querySelector('.animal-species-name') ?? null;
   }

   static decorateSpeciesDialog(dialog, title) {
      if (!title) {
         return;
      }

      const scrollRegion = dialog.querySelector('.species-overlay-scroll');

      if (!scrollRegion) {
         return;
      }

      scrollRegion.setAttribute('tabindex', '0');
      scrollRegion.setAttribute('role', 'region');
      scrollRegion.setAttribute('aria-labelledby', SpeciesOverlayModal.TITLE_ID);
   }
}
