import { CenterPanHelpers } from './centerPanHelpers.js';

export class Center {
   static centerMarkerWithContain(panzoom, markerEl, viewportEl) {
      if (!panzoom || !markerEl || !viewportEl) return;

      const prevContain = panzoom?.options?.contain ?? CenterPanHelpers.DEFAULT_CONTAIN;

      const markerRect = markerEl.getBoundingClientRect();
      const viewportRect = viewportEl.getBoundingClientRect();

      const markerCenterX = markerRect.left + markerRect.width / 2;
      const markerCenterY = markerRect.top + markerRect.height / 2;

      const viewportCenterX = viewportRect.left + viewportRect.width / 2;
      const viewportCenterY = viewportRect.top + viewportRect.height / 2;

      const dx = viewportCenterX - markerCenterX;
      const dy = viewportCenterY - markerCenterY;

      const scale = (typeof panzoom.getScale === 'function' ? panzoom.getScale() : 1) || 1;
      const panDx = dx / scale;
      const panDy = dy / scale;

      const pan = CenterPanHelpers.getPanXY(panzoom);
      const targetX = pan.x + panDx;
      const targetY = pan.y + panDy;

      CenterPanHelpers.setContain(panzoom, CenterPanHelpers.FOCUS_CONTAIN);
      panzoom.pan(targetX, targetY, { animate: false });

      CenterPanHelpers.setContain(panzoom, prevContain);
      panzoom.pan(targetX, targetY, { animate: false });
      CenterPanHelpers.clampNow(panzoom);
   }
}
