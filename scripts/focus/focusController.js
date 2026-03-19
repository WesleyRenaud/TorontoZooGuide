import { TYPE_REGISTRY } from '../tooltips/tooltipRenderers.js';
import { centerMarkerWithContain } from './center.js';
import { coordKey } from '../utils/coords.js';

function itemLikelihood(item) {
   const v = Number(item?.likelihood);
   return Number.isFinite(v) ? v : -1;
}

function distToViewportCenter(markerEl, viewportEl) {
   const mr = markerEl.getBoundingClientRect();
   const vr = viewportEl.getBoundingClientRect();

   const mx = mr.left + mr.width / 2;
   const my = mr.top + mr.height / 2;

   const vx = vr.left + vr.width / 2;
   const vy = vr.top + vr.height / 2;

   const dx = mx - vx;
   const dy = my - vy;
   return Math.hypot(dx, dy);
   }

   export function createFocusController({
      panzoom,
      getMarkerByCoord,
      getViewportEl,
      tooltip,
      getAllMarkers,
   }) {
   async function focus({ row, type }) {
      if (!row) return;

      const x = row.x_coord ?? row.x ?? row.X ?? null;
      const y = row.y_coord ?? row.y ?? row.Y ?? null;

      const typeKey = String(type || row.type || '');
      const renderer = TYPE_REGISTRY?.[typeKey] ?? TYPE_REGISTRY?.animal ?? null;

      const matchFn = renderer?.isMatch
         ? (item) => renderer.isMatch(item, row)
         : () => true;

      if (x != null && y != null) {
         focusByCoord(x, y, matchFn);
         return;
      }

      focusByScan(matchFn, typeKey);
   }

   function focusByCoord(x, y, matchFn) {
      const key = coordKey(x, y);
      const marker = getMarkerByCoord(key);
      if (!marker) return;

      const viewport = getViewportEl();
      if (!viewport) return;

      panzoom.zoom(3, { animate: false });

      requestAnimationFrame(() => {
         centerMarkerWithContain(panzoom, marker, viewport);

         requestAnimationFrame(() => {
         centerMarkerWithContain(panzoom, marker, viewport);

         const items = marker.__items || [];
         tooltip.open(marker, items);
         tooltip.jumpTo(matchFn);
         });
      });
   }

   function focusByScan(matchFn, typeKey) {
      const viewport = getViewportEl();
      if (!viewport) return;

      const markers = (typeof getAllMarkers === 'function' ? getAllMarkers() : []) || [];
      if (!markers.length) return;

      let best = null;

      for (const marker of markers) {
         const items = marker.__items || [];
         if (!items.length) continue;

         const matches = [];
         for (let i = 0; i < items.length; i++) {
         const it = items[i];
         if (String(it?.type || '') !== typeKey) continue;
         if (matchFn(it)) matches.push(it);
         }
         if (!matches.length) continue;

         const d = distToViewportCenter(marker, viewport);

         let bestHereScore = -Infinity;
         for (const it of matches) {
         const lik = itemLikelihood(it);
         const score = (lik * 1000) - d;
         if (score > bestHereScore) bestHereScore = score;
         }

         if (!best || bestHereScore > best.score) {
         best = { marker, items, score: bestHereScore };
         }
      }

      if (!best) return;

      panzoom.zoom(3, { animate: false });

      requestAnimationFrame(() => {
         centerMarkerWithContain(panzoom, best.marker, viewport);

         requestAnimationFrame(() => {
         centerMarkerWithContain(panzoom, best.marker, viewport);

         tooltip.open(best.marker, best.items);
         tooltip.jumpTo(matchFn);
         });
      });
   }

   return { focus };
}