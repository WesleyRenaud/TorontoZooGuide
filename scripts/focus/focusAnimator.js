import { Center } from './center.js';

const FOCUS_ZOOM_LEVEL = 3;

export class FocusAnimator {
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

      panzoom.zoom(FOCUS_ZOOM_LEVEL, { animate: false });

      requestAnimationFrame(() => {
         Center.centerMarkerWithContain(panzoom, marker, viewportEl);

         requestAnimationFrame(() => {
            Center.centerMarkerWithContain(panzoom, marker, viewportEl);

            tooltip.open(marker, items || marker.__items || []);
            tooltip.jumpTo(matchFn);
         });
      });
   }
}
