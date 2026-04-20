import { focusMarker } from './focusAnimator.js';
import {
   createFocusMatch,
   findBestMarkerByScan,
   findMarkerByCoordinates,
} from './focusTargetFinder.js';

export function createFocusController({
   panzoom,
   getMarkerByCoord,
   getViewportEl,
   tooltip,
   getAllMarkers,
}) {
   function focusByCoord(x, y, matchFn) {
      const marker = findMarkerByCoordinates({
         x,
         y,
         getMarkerByCoord,
      });

      if (!marker) {
         return;
      }

      const viewportEl = getViewportEl();

      if (!viewportEl) {
         return;
      }

      focusMarker({
         panzoom,
         marker,
         viewportEl,
         tooltip,
         matchFn,
         items: marker.__items || [],
      });
   }

   function focusByScan(typeKey, matchFn) {
      const viewportEl = getViewportEl();

      if (!viewportEl) {
         return;
      }

      const markers = (
         typeof getAllMarkers === 'function'
            ? getAllMarkers()
            : []
      ) || [];

      if (!markers.length) {
         return;
      }

      const best = findBestMarkerByScan({
         typeKey,
         matchFn,
         markers,
         viewportEl,
      });

      if (!best) {
         return;
      }

      focusMarker({
         panzoom,
         marker: best.marker,
         viewportEl,
         tooltip,
         matchFn,
         items: best.items,
      });
   }

   async function focus({ row, type }) {
      if (!row) {
         return;
      }

      const x = row.x_coord ?? null;
      const y = row.y_coord ?? null;

      const { typeKey, matchFn } = createFocusMatch(row, type);

      if (x != null && y != null) {
         focusByCoord(x, y, matchFn);
         return;
      }

      focusByScan(typeKey, matchFn);
   }

   return { focus };
}
