// center.js
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

// Forces Panzoom to re-apply contain constraints immediately
function clampNow(panzoom) {
   const p = getPanXY(panzoom);
   panzoom.pan(p.x, p.y, { animate: false });
}

export function centerMarkerWithContain(panzoom, markerEl, viewportEl) {
   if (!panzoom || !markerEl || !viewportEl) return;

   const prevContain = panzoom?.options?.contain ?? DEFAULT_CONTAIN;

   // --- compute target pan (same as you had) ---
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

   // --- atomic application (NO rAF) ---
   // 1) temporarily allow overscroll (not painted yet)
   setContain(panzoom, FOCUS_CONTAIN);
   panzoom.pan(targetX, targetY, { animate: false });

   // 2) immediately restore contain and re-pan to force clamp BEFORE next paint
   setContain(panzoom, prevContain);
   panzoom.pan(targetX, targetY, { animate: false });
   clampNow(panzoom);
}