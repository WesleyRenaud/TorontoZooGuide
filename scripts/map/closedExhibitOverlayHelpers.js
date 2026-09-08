import { AssetKeyNormalizer } from '../assets/assetKeyNormalizer.js';

export class ClosedExhibitOverlayHelpers {
   static CLOSED_EXHIBIT_OVERLAY_ID_PREFIX = 'closed-exhibit-overlay-';

   static CLOSED_EXHIBIT_OVERLAY_SELECTOR = `[id^="${ClosedExhibitOverlayHelpers.CLOSED_EXHIBIT_OVERLAY_ID_PREFIX}"]`;

   static getClosedExhibitOverlays() {
      return document.querySelectorAll(ClosedExhibitOverlayHelpers.CLOSED_EXHIBIT_OVERLAY_SELECTOR);
   }

   static hideClosedExhibitOverlays(overlays) {
      overlays.forEach((overlay) => {
         overlay.style.display = 'none';
      });
   }

   static getClosedExhibitOverlayId(exhibitKey) {
      return `${ClosedExhibitOverlayHelpers.CLOSED_EXHIBIT_OVERLAY_ID_PREFIX}${exhibitKey}`;
   }

   static showClosedExhibitOverlay(exhibitKey) {
      const overlay = document.getElementById(
         ClosedExhibitOverlayHelpers.getClosedExhibitOverlayId(exhibitKey)
      );

      if (overlay) {
         overlay.style.display = '';
      }
   }

   static normalizeClosedExhibitKeys(closedExhibits) {
      return Array.isArray(closedExhibits)
         ? closedExhibits
            .map(AssetKeyNormalizer.normalize)
            .filter(Boolean)
         : [];
   }
}
