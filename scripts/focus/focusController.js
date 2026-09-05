import { FocusAnimator } from './focusAnimator.js';
import { FocusTargetFinder } from './focusTargetFinder.js';

export function createFocusController({
   panzoom,
   getMarkerByCoord,
   getViewportEl,
   tooltip,
   getAllMarkers,
}) {
   function getViewport() {
      return typeof getViewportEl === 'function'
         ? getViewportEl()
         : null;
   }

   function getMarkers() {
      return (
         typeof getAllMarkers === 'function'
            ? getAllMarkers()
            : []
      ) || [];
   }

   function focusResolvedTarget(target, matchFn, viewportEl) {
      if (!target?.marker || !viewportEl) {
         return;
      }

      FocusAnimator.focusMarker({
         panzoom,
         marker: target.marker,
         viewportEl,
         tooltip,
         matchFn,
         items: target.items,
      });
   }

   function resolveTargetByCoordinates(x, y) {
      const marker = FocusTargetFinder.findMarkerByCoordinates({
         x,
         y,
         getMarkerByCoord,
      });

      if (!marker) {
         return null;
      }

      return {
         marker,
         items: marker.__items || [],
      };
   }

   function resolveTargetByScan(typeKey, matchFn, viewportEl) {
      const markers = getMarkers();

      if (!markers.length || !viewportEl) {
         return null;
      }

      return FocusTargetFinder.findBestMarkerByScan({
         typeKey,
         matchFn,
         markers,
         viewportEl,
      });
   }

   function resolveFocusTarget(row, typeKey, matchFn, viewportEl) {
      const x = row.x_coord ?? null;
      const y = row.y_coord ?? null;

      if (x != null && y != null) {
         return resolveTargetByCoordinates(x, y);
      }

      return resolveTargetByScan(typeKey, matchFn, viewportEl);
   }

   function focus({ row, type }) {
      if (!row) {
         return;
      }

      const viewportEl = getViewport();

      if (!viewportEl) {
         return;
      }

      const { typeKey, matchFn } = FocusTargetFinder.createFocusMatch(row, type);
      const target = resolveFocusTarget(row, typeKey, matchFn, viewportEl);

      if (!target) {
         return;
      }

      focusResolvedTarget(target, matchFn, viewportEl);
   }

   return { focus };
}
