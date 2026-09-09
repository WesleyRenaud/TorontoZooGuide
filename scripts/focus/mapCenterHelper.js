import { CenterPanHelper } from './centerPanHelper.js';
import { AppConfig } from '../config/appConfig.js';

export class MapCenterHelper {
   static centerMarkerWithContain(panzoom, markerEl, viewportEl) {
      if (!panzoom || !markerEl || !viewportEl) return;

      const prevContain = panzoom?.options?.contain ?? AppConfig.DEFAULT_MAP_CONTAIN;

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

      const pan = CenterPanHelper.getPanXY(panzoom);
      const targetX = pan.x + panDx;
      const targetY = pan.y + panDy;

      CenterPanHelper.setContain(panzoom, CenterPanHelper.FOCUS_CONTAIN);
      panzoom.pan(targetX, targetY, { animate: false });

      CenterPanHelper.setContain(panzoom, prevContain);
      panzoom.pan(targetX, targetY, { animate: false });
      CenterPanHelper.clampNow(panzoom);
   }
}
