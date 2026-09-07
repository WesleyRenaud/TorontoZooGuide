import { ClosedExhibitOverlayHelpers } from './closedExhibitOverlayHelpers.js';

export class ClosedExhibitOverlay {
   static setClosedExhibitOverlaysVisible(closedExhibits) {
      const overlays = ClosedExhibitOverlayHelpers.getClosedExhibitOverlays();
      const closedExhibitKeys = ClosedExhibitOverlayHelpers.normalizeClosedExhibitKeys(closedExhibits);

      ClosedExhibitOverlayHelpers.hideClosedExhibitOverlays(overlays);

      closedExhibitKeys.forEach((key) => {
         ClosedExhibitOverlayHelpers.showClosedExhibitOverlay(key);
      });
   }

   static async syncClosedExhibitOverlays(sources, ctx) {
      const src = sources.closedExhibit;

      if (!src?.fetch) {
         ClosedExhibitOverlay.setClosedExhibitOverlaysVisible([]);
         return [];
      }

      try {
         const rows = await src.fetch(ctx);
         const closedExhibits = ClosedExhibitOverlayHelpers.normalizeClosedExhibitKeys(rows);

         ClosedExhibitOverlay.setClosedExhibitOverlaysVisible(closedExhibits);
         return closedExhibits;
      } catch {
         ClosedExhibitOverlay.setClosedExhibitOverlaysVisible([]);
         return [];
      }
   }
}
