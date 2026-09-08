import { MapCenterHelper } from './mapCenterHelper.js';

export class FocusAnimator {
   static FOCUS_ZOOM_LEVEL = 3;

   static focusMarker({
      panzoom,
      marker,
      viewportEl,
      tooltip,
      matchFn,
      items,
   }) {
      if (!panzoom || !marker || !viewportEl || !tooltip) {
         return;
      }

      panzoom.zoom(FocusAnimator.FOCUS_ZOOM_LEVEL, { animate: false });

      requestAnimationFrame(() => {
         MapCenterHelper.centerMarkerWithContain(panzoom, marker, viewportEl);

         requestAnimationFrame(() => {
            MapCenterHelper.centerMarkerWithContain(panzoom, marker, viewportEl);

            tooltip.open(marker, items || marker.__items || []);
            tooltip.jumpTo(matchFn);
         });
      });
   }
}
