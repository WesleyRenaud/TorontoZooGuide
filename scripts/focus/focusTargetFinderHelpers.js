export class FocusTargetFinderHelpers {
   static itemLikelihood(item) {
      const value = Number(item?.likelihood);
      return Number.isFinite(value) ? value : -1;
   }

   static distToViewportCenter(markerEl, viewportEl) {
      const markerRect = markerEl.getBoundingClientRect();
      const viewportRect = viewportEl.getBoundingClientRect();

      const markerCenterX = markerRect.left + markerRect.width / 2;
      const markerCenterY = markerRect.top + markerRect.height / 2;

      const viewportCenterX = viewportRect.left + viewportRect.width / 2;
      const viewportCenterY = viewportRect.top + viewportRect.height / 2;

      const dx = markerCenterX - viewportCenterX;
      const dy = markerCenterY - viewportCenterY;

      return Math.hypot(dx, dy);
   }
}
