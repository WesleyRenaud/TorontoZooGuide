export class CenterPanHelper {
   static DEFAULT_CONTAIN = 'outside';
   static FOCUS_CONTAIN = 'none';

   static setContain(panzoom, mode) {
      if (!panzoom) return;
      if (panzoom.options) panzoom.options.contain = mode;
      if (typeof panzoom.setOptions === 'function') panzoom.setOptions({ contain: mode });
   }

   static getPanXY(panzoom) {
      const p = (typeof panzoom.getPan === 'function' ? panzoom.getPan() : null) || {};
      const x = Number.isFinite(p.x) ? p.x : (Number.isFinite(p.panX) ? p.panX : 0);
      const y = Number.isFinite(p.y) ? p.y : (Number.isFinite(p.panY) ? p.panY : 0);
      return { x, y };
   }

   static clampNow(panzoom) {
      const p = CenterPanHelper.getPanXY(panzoom);
      panzoom.pan(p.x, p.y, { animate: false });
   }
}
