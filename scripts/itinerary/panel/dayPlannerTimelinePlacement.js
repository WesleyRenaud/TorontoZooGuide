export function readCssLengthPx(style, property) {
   if (!style?.getPropertyValue) {
      return null;
   }

   const rawValue = style.getPropertyValue(property).trim();

   if (!rawValue) {
      return null;
   }

   const parsedValue = Number.parseFloat(rawValue);

   return Number.isFinite(parsedValue) && parsedValue > 0 ? parsedValue : null;
}

export function resolveTimelineElement(gridLine) {
   if (!gridLine) {
      return null;
   }

   if (typeof gridLine.closest === 'function') {
      return gridLine.closest('.itinerary-day-timeline');
   }

   let current = gridLine.parentElement ?? gridLine.parent;

   while (current) {
      if (current.classList?.contains('itinerary-day-timeline')) {
         return current;
      }

      current = current.parentElement ?? current.parent;
   }

   return null;
}

export function parseStripTopOffsetFromProbeTop(topPx) {
   return Number.isFinite(topPx) && topPx < 0
      ? Math.abs(topPx)
      : null;
}

export function computePointPillVerticalSpanFraction(slotHeight, pillHeight) {
   if (!slotHeight || !pillHeight) {
      return null;
   }

   return pillHeight / slotHeight;
}

export function computePointPillStripPlacementBand({
   slotHeight,
   pillHeight,
   stripTopOffset,
   offsetFraction = 0,
}) {
   if (!slotHeight || !pillHeight || !stripTopOffset) {
      return {
         offsetFraction,
         durationFraction: 0,
      };
   }

   const topPx = (offsetFraction * slotHeight) - stripTopOffset;

   return {
      offsetFraction: topPx / slotHeight,
      durationFraction: pillHeight / slotHeight,
   };
}
