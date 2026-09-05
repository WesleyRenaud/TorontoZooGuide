import { AssetKeyNormalizer } from '../assets/assetKeyNormalizer.js';

const CLOSED_EXHIBIT_OVERLAY_ID_PREFIX = 'closed-exhibit-overlay-';
const CLOSED_EXHIBIT_OVERLAY_SELECTOR = `[id^="${CLOSED_EXHIBIT_OVERLAY_ID_PREFIX}"]`;

function getClosedExhibitOverlays() {
   return document.querySelectorAll(CLOSED_EXHIBIT_OVERLAY_SELECTOR);
}

function hideClosedExhibitOverlays(overlays) {
   overlays.forEach((overlay) => {
      overlay.style.display = 'none';
   });
}

function getClosedExhibitOverlayId(exhibitKey) {
   return `${CLOSED_EXHIBIT_OVERLAY_ID_PREFIX}${exhibitKey}`;
}

function showClosedExhibitOverlay(exhibitKey) {
   const overlay = document.getElementById(
      getClosedExhibitOverlayId(exhibitKey)
   );

   if (overlay) {
      overlay.style.display = '';
   }
}

function normalizeClosedExhibitKeys(closedExhibits) {
   return Array.isArray(closedExhibits)
      ? closedExhibits
         .map(AssetKeyNormalizer.normalize)
         .filter(Boolean)
      : [];
}

export class ClosedExhibitOverlay {
   static setClosedExhibitOverlaysVisible(closedExhibits) {
      const overlays = getClosedExhibitOverlays();
      const closedExhibitKeys = normalizeClosedExhibitKeys(closedExhibits);

      hideClosedExhibitOverlays(overlays);

      closedExhibitKeys.forEach((key) => {
         showClosedExhibitOverlay(key);
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
         const closedExhibits = normalizeClosedExhibitKeys(rows);

         ClosedExhibitOverlay.setClosedExhibitOverlaysVisible(closedExhibits);
         return closedExhibits;
      } catch {
         ClosedExhibitOverlay.setClosedExhibitOverlaysVisible([]);
         return [];
      }
   }
}
