const DEFAULT_CONTAIN = 'outside';
const FOCUS_CONTAIN = 'none';

function setContain(panzoom, mode) {
   if (!panzoom) return;
   if (panzoom.options) panzoom.options.contain = mode;
   if (typeof panzoom.setOptions === 'function') panzoom.setOptions({ contain: mode });
}

function getPanXY(panzoom) {
   const p = (typeof panzoom.getPan === 'function' ? panzoom.getPan() : null) || {};
   const x = Number.isFinite(p.x) ? p.x : (Number.isFinite(p.panX) ? p.panX : 0);
   const y = Number.isFinite(p.y) ? p.y : (Number.isFinite(p.panY) ? p.panY : 0);
   return { x, y };
}

function clampNow(panzoom) {
   const p = getPanXY(panzoom);
   panzoom.pan(p.x, p.y, { animate: false });
}

export function centerMarkerWithContain(panzoom, markerEl, viewportEl) {
   if (!panzoom || !markerEl || !viewportEl) return;

   const prevContain = panzoom?.options?.contain ?? DEFAULT_CONTAIN;

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

   const pan = getPanXY(panzoom);
   const targetX = pan.x + panDx;
   const targetY = pan.y + panDy;

   setContain(panzoom, FOCUS_CONTAIN);
   panzoom.pan(targetX, targetY, { animate: false });

   setContain(panzoom, prevContain);
   panzoom.pan(targetX, targetY, { animate: false });
   clampNow(panzoom);
}