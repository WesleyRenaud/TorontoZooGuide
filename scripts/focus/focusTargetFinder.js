import { FocusTargetFinderHelper } from './focusTargetFinderHelper.js';
import { CoordKey } from '../map/coordKey.js';
import { TooltipRenderer } from '../tooltips/tooltipRenderer.js';

export class FocusTargetFinder {
   static createFocusMatch(row, type) {
      const typeKey = String(type || row?.type || '');
      const renderer = TooltipRenderer.TYPE_REGISTRY?.[typeKey]
         ?? TooltipRenderer.TYPE_REGISTRY?.animal
         ?? null;

      const matchFn = renderer?.isMatch
         ? (item) => renderer.isMatch(item, row)
         : () => true;

      return {
         typeKey,
         matchFn,
      };
   }

   static findMarkerByCoordinates({ x, y, getMarkerByCoord }) {
      const key = CoordKey.coordKey(x, y);

      if (!key) {
         return null;
      }

      return getMarkerByCoord(key) || null;
   }

   static findBestMarkerByScan({
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

         const distance = FocusTargetFinderHelper.distToViewportCenter(marker, viewportEl);

         let bestScoreHere = -Infinity;

         for (const item of matches) {
            const score = (FocusTargetFinderHelper.itemLikelihood(item) * 1000) - distance;
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
}
