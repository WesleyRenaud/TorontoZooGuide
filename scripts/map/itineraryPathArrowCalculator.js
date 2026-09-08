import { SvgPathParser } from './svgPathParser.js';

export class ItineraryPathArrowCalculator {
   static cubicBezierPoint(t, start, controlPoint1, controlPoint2, end) {
      const inverse = 1 - t;
      const inverseSquared = inverse * inverse;
      const tSquared = t * t;

      return {
         x:
            inverseSquared * inverse * start.x
            + 3 * inverseSquared * t * controlPoint1.x
            + 3 * inverse * tSquared * controlPoint2.x
            + tSquared * t * end.x,
         y:
            inverseSquared * inverse * start.y
            + 3 * inverseSquared * t * controlPoint1.y
            + 3 * inverse * tSquared * controlPoint2.y
            + tSquared * t * end.y,
      };
   }

   static appendCubicBezierSamples(
      polyline,
      start,
      controlPoint1,
      controlPoint2,
      end,
      stepPx
   ) {
      const chordLength = Math.hypot(end.x - start.x, end.y - start.y);
      const steps = Math.max(2, Math.ceil(chordLength / stepPx));

      for (let step = 1; step <= steps; step += 1) {
         polyline.push(
            ItineraryPathArrowCalculator.cubicBezierPoint(step / steps, start, controlPoint1, controlPoint2, end)
         );
      }
   }

   static polylineLength(polyline) {
      let length = 0;

      for (let index = 1; index < polyline.length; index += 1) {
         length += Math.hypot(
            polyline[index].x - polyline[index - 1].x,
            polyline[index].y - polyline[index - 1].y
         );
      }

      return length;
   }

   static pointAndTangentAtDistance(polyline, distancePx) {
      let remaining = distancePx;

      for (let index = 1; index < polyline.length; index += 1) {
         const start = polyline[index - 1];
         const end = polyline[index];
         const segmentLength = Math.hypot(end.x - start.x, end.y - start.y);

         if (segmentLength === 0) {
            continue;
         }

         if (remaining <= segmentLength) {
            const ratio = remaining / segmentLength;

            return {
               x: start.x + (end.x - start.x) * ratio,
               y: start.y + (end.y - start.y) * ratio,
               angleDeg: Math.atan2(end.y - start.y, end.x - start.x) * (180 / Math.PI),
            };
         }

         remaining -= segmentLength;
      }

      return null;
   }

   static mergeConnectedPolylines(polylines, tolerance = 1.5) {
      if (polylines.length === 0) {
         return [];
      }

      const merged = [polylines[0].slice()];

      for (let index = 1; index < polylines.length; index += 1) {
         const current = polylines[index];
         const previous = merged[merged.length - 1];
         const previousEnd = previous[previous.length - 1];
         const currentStart = current[0];

         if (SvgPathParser.pointsNear(previousEnd, currentStart, tolerance)) {
            previous.push(...current.slice(1));
         }
         else {
            merged.push(current.slice());
         }
      }

      return merged;
   }

   static buildPathArrowPlacementsForPolyline(polyline, {
      intervalPx,
      skipEndPx,
      minPathLengthPx,
   }) {
      const totalLength = ItineraryPathArrowCalculator.polylineLength(polyline);

      if (totalLength < minPathLengthPx) {
         return [];
      }

      const placements = [];

      for (
         let distance = intervalPx;
         distance < totalLength - skipEndPx;
         distance += intervalPx
      ) {
         if (distance < skipEndPx) {
            continue;
         }

         const placement = ItineraryPathArrowCalculator.pointAndTangentAtDistance(polyline, distance);

         if (placement != null) {
            placements.push(placement);
         }
      }

      return placements;
   }
}
