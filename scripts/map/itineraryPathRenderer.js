import { ItineraryPathArrowCalculator } from './itineraryPathArrowCalculator.js';
import { ItineraryPathConstants } from './itineraryPathConstants.js';
import { SvgPathParser } from './svgPathParser.js';

export class ItineraryPathRenderer {
   static buildPathPolylines(pathD, stepPx = 8) {
      const segments = SvgPathParser.parseSvgPathD(pathD);

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
            ItineraryPathArrowCalculator.appendCubicBezierSamples(
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
      const polylines = ItineraryPathArrowCalculator.mergeConnectedPolylines(
         ItineraryPathRenderer.buildPathPolylines(pathD, curveSampleStepPx)
      );

      return polylines.flatMap((polyline) => ItineraryPathArrowCalculator.buildPathArrowPlacementsForPolyline(
         polyline,
         {
            intervalPx,
            skipEndPx,
            minPathLengthPx,
         }
      ));
   }
}
