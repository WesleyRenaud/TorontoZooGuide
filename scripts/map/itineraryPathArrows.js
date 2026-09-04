import { ItineraryPathConstants } from './itineraryPathConstants.js';
import { SvgPathParsing } from './svgPathParsing.js';

function cubicBezierPoint(t, start, controlPoint1, controlPoint2, end) {
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

function appendCubicBezierSamples(
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
         cubicBezierPoint(step / steps, start, controlPoint1, controlPoint2, end)
      );
   }
}

function polylineLength(polyline) {
   let length = 0;

   for (let index = 1; index < polyline.length; index += 1) {
      length += Math.hypot(
         polyline[index].x - polyline[index - 1].x,
         polyline[index].y - polyline[index - 1].y
      );
   }

   return length;
}

function pointAndTangentAtDistance(polyline, distancePx) {
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

function mergeConnectedPolylines(polylines, tolerance = 1.5) {
   if (polylines.length === 0) {
      return [];
   }

   const merged = [polylines[0].slice()];

   for (let index = 1; index < polylines.length; index += 1) {
      const current = polylines[index];
      const previous = merged[merged.length - 1];
      const previousEnd = previous[previous.length - 1];
      const currentStart = current[0];

      if (SvgPathParsing.pointsNear(previousEnd, currentStart, tolerance)) {
         previous.push(...current.slice(1));
      }
      else {
         merged.push(current.slice());
      }
   }

   return merged;
}

function buildPathArrowPlacementsForPolyline(polyline, {
   intervalPx,
   skipEndPx,
   minPathLengthPx,
}) {
   const totalLength = polylineLength(polyline);

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

      const placement = pointAndTangentAtDistance(polyline, distance);

      if (placement != null) {
         placements.push(placement);
      }
   }

   return placements;
}

export class ItineraryPathArrows {
   static buildPathPolylines(pathD, stepPx = 8) {
      const segments = SvgPathParsing.parseSvgPathD(pathD);

      if (segments.length === 0) {
         return [];
      }

      const polylines = [];
      let polyline = [];
      let currentPoint = null;

      function finishPolyline() {
         if (polyline.length >= 2) {
            polylines.push(polyline);
         }

         polyline = [];
         currentPoint = null;
      }

      for (const segment of segments) {
         if (segment.tag === 'M') {
            finishPolyline();
            currentPoint = { x: segment.x, y: segment.y };
            polyline.push(currentPoint);
            continue;
         }

         if (currentPoint == null) {
            continue;
         }

         if (segment.tag === 'L' || segment.tag === 'H' || segment.tag === 'V') {
            currentPoint = { x: segment.x, y: segment.y };
            polyline.push(currentPoint);
            continue;
         }

         if (segment.tag === 'C') {
            const end = { x: segment.x, y: segment.y };
            appendCubicBezierSamples(
               polyline,
               currentPoint,
               {
                  x: segment.controlPoint1X,
                  y: segment.controlPoint1Y,
               },
               {
                  x: segment.controlPoint2X,
                  y: segment.controlPoint2Y,
               },
               end,
               stepPx
            );
            currentPoint = end;
         }
      }

      finishPolyline();

      return polylines;
   }

   static offsetArrowPlacement(placement, offsetPx, side = 'left') {
      const angleRadians = placement.angleDeg * (Math.PI / 180);
      const sign = side === 'left' ? 1 : -1;
      const offsetX = -Math.sin(angleRadians) * sign * offsetPx;
      const offsetY = Math.cos(angleRadians) * sign * offsetPx;

      return {
         x: placement.x + offsetX,
         y: placement.y + offsetY,
         angleDeg: placement.angleDeg,
      };
   }

   static buildPathArrowPlacements(pathD, {
      intervalPx = ItineraryPathConstants.ITINERARY_PATH_ARROW_INTERVAL_PX,
      skipEndPx = ItineraryPathConstants.ITINERARY_PATH_ARROW_SKIP_END_PX,
      curveSampleStepPx = ItineraryPathConstants.ITINERARY_PATH_ARROW_CURVE_SAMPLE_STEP_PX,
      minPathLengthPx = ItineraryPathConstants.ITINERARY_PATH_ARROW_MIN_PATH_LENGTH_PX,
   } = {}) {
      const polylines = mergeConnectedPolylines(
         ItineraryPathArrows.buildPathPolylines(pathD, curveSampleStepPx)
      );

      return polylines.flatMap((polyline) => buildPathArrowPlacementsForPolyline(
         polyline,
         {
            intervalPx,
            skipEndPx,
            minPathLengthPx,
         }
      ));
   }
}
