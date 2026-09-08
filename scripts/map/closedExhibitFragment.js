import { ClosedExhibitOverlayHelper } from './closedExhibitOverlayHelper.js';

export class ClosedExhibitFragment {
   static setClosedExhibitOverlaysVisible(closedExhibits) {
      const overlays = ClosedExhibitOverlayHelper.getClosedExhibitOverlays();
      const closedExhibitKeys = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys(closedExhibits);

      ClosedExhibitOverlayHelper.hideClosedExhibitOverlays(overlays);

      closedExhibitKeys.forEach((key) => {
         ClosedExhibitOverlayHelper.showClosedExhibitOverlay(key);
      });
   }

   static async syncClosedExhibitOverlays(sources, ctx) {
      const src = sources.closedExhibit;

      if (!src?.fetch) {
         ClosedExhibitFragment.setClosedExhibitOverlaysVisible([]);
         return [];
      }

      try {
         const rows = await src.fetch(ctx);
         const closedExhibits = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys(rows);

         ClosedExhibitFragment.setClosedExhibitOverlaysVisible(closedExhibits);
         return closedExhibits;
      } catch {
         ClosedExhibitFragment.setClosedExhibitOverlaysVisible([]);
         return [];
      }
   }
}
