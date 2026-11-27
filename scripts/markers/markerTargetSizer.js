export class MarkerTargetSizer {
   static WCAG_MIN_TARGET_PX = 24;
   static TARGET_SIZE_PROPERTY = '--marker-target-size';

   static readCenter(markerEl) {
      return {
         x: markerEl.offsetLeft ?? 0,
         y: markerEl.offsetTop ?? 0,
      };
   }

   static findNearestDistance(centers, index) {
      let nearest = Infinity;

      centers.forEach((other, otherIndex) => {
         if (otherIndex === index) {
            return;
         }

         const distance = Math.hypot(
            other.x - centers[index].x,
            other.y - centers[index].y
         );

         nearest = Math.min(nearest, distance);
      });

      return nearest;
   }

   // Capped at the nearest pin's distance so neighbouring hit areas never overlap.
   static computeTargetSizes(centers, minTargetPx = MarkerTargetSizer.WCAG_MIN_TARGET_PX) {
      return centers.map((center, index) => {
         const nearest = MarkerTargetSizer.findNearestDistance(centers, index);

         return Math.min(minTargetPx, nearest);
      });
   }

   static applyToMarkers(markerEls) {
      const centers = markerEls.map(MarkerTargetSizer.readCenter);
      const sizes = MarkerTargetSizer.computeTargetSizes(centers);

      markerEls.forEach((markerEl, index) => {
         markerEl.style.setProperty(MarkerTargetSizer.TARGET_SIZE_PROPERTY, `${sizes[index]}px`);
      });
   }
}
