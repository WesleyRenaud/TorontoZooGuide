import { CoordKey } from '../map/coordKey.js';
import { TooltipRenderers } from '../tooltips/tooltipRenderers.js';

function itemLikelihood(item) {
   const value = Number(item?.likelihood);
   return Number.isFinite(value) ? value : -1;
}

function distToViewportCenter(markerEl, viewportEl) {
   const markerRect = markerEl.getBoundingClientRect();
   const viewportRect = viewportEl.getBoundingClientRect();

   const markerCenterX = markerRect.left + markerRect.width / 2;
   const markerCenterY = markerRect.top + markerRect.height / 2;

   const viewportCenterX = viewportRect.left + viewportRect.width / 2;
   const viewportCenterY = viewportRect.top + viewportRect.height / 2;

   const dx = markerCenterX - viewportCenterX;
   const dy = markerCenterY - viewportCenterY;

   return Math.hypot(dx, dy);
}

export function createFocusMatch(row, type) {
   const typeKey = String(type || row?.type || '');
   const renderer = TooltipRenderers.TYPE_REGISTRY?.[typeKey]
      ?? TooltipRenderers.TYPE_REGISTRY?.animal
      ?? null;

   const matchFn = renderer?.isMatch
      ? (item) => renderer.isMatch(item, row)
      : () => true;

   return {
      typeKey,
      matchFn,
   };
}

export function findMarkerByCoordinates({ x, y, getMarkerByCoord }) {
   const key = CoordKey.coordKey(x, y);

   if (!key) {
      return null;
   }

   return getMarkerByCoord(key) || null;
}

export function findBestMarkerByScan({
   typeKey,
   matchFn,
   markers,
   viewportEl,
}) {
   let best = null;

   for (const marker of markers) {
      const items = marker.__items || [];

      if (!items.length) {
         continue;
      }

      const matches = items.filter((item) => (
         String(item?.type || '') === typeKey &&
         matchFn(item)
      ));

      if (!matches.length) {
         continue;
      }

      const distance = distToViewportCenter(marker, viewportEl);

      let bestScoreHere = -Infinity;

      for (const item of matches) {
         const score = (itemLikelihood(item) * 1000) - distance;
         if (score > bestScoreHere) {
            bestScoreHere = score;
         }
      }

      if (!best || bestScoreHere > best.score) {
         best = {
            marker,
            items,
            score: bestScoreHere,
         };
      }
   }

   return best;
}
