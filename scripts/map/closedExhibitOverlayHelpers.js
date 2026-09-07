import { AssetKeyNormalizer } from '../assets/assetKeyNormalizer.js';

const CLOSED_EXHIBIT_OVERLAY_ID_PREFIX = 'closed-exhibit-overlay-';

const CLOSED_EXHIBIT_OVERLAY_SELECTOR = `[id^="${CLOSED_EXHIBIT_OVERLAY_ID_PREFIX}"]`;

export class ClosedExhibitOverlayHelpers {
   static getClosedExhibitOverlays() {
      return document.querySelectorAll(CLOSED_EXHIBIT_OVERLAY_SELECTOR);
   }

   static hideClosedExhibitOverlays(overlays) {
      overlays.forEach((overlay) => {
         overlay.style.display = 'none';
      });
   }

   static getClosedExhibitOverlayId(exhibitKey) {
      return `${CLOSED_EXHIBIT_OVERLAY_ID_PREFIX}${exhibitKey}`;
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
