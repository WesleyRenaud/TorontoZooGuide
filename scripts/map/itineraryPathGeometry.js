import {
   buildPathDFromWalkGraphSegments,
   getWalkGraphPathSegments,
} from './walkGraphPathGeometry.js';

export { parseSvgPathD, pointsNear } from './svgPathParsing.js';
export {
   buildPathDFromWalkGraphSegments,
   getWalkGraphPathSegments,
   resetWalkGraphPathCache,
} from './walkGraphPathGeometry.js';
export {
   buildPathArrowPlacements,
   buildPathPolylines,
   offsetArrowPlacement,
} from './itineraryPathArrows.js';

export function buildSmoothedPathD(points, { tension = 0.38 } = {}) {
   if (points.length < 2) {
      return '';
   }

   if (points.length === 2) {
      const [start, end] = points;

      return `M ${start.x} ${start.y} L ${end.x} ${end.y}`;
   }

   const scale = Math.max(0, Math.min(1, tension));
   const pathParts = [`M ${points[0].x} ${points[0].y}`];

   for (let index = 0; index < points.length - 1; index += 1) {
      const previous = points[Math.max(0, index - 1)];
      const current = points[index];
      const next = points[index + 1];
      const following = points[Math.min(points.length - 1, index + 2)];

      const controlPoint1X = current.x + ((next.x - previous.x) / 6) * scale;
      const controlPoint1Y = current.y + ((next.y - previous.y) / 6) * scale;
      const controlPoint2X = next.x - ((following.x - current.x) / 6) * scale;
      const controlPoint2Y = next.y - ((following.y - current.y) / 6) * scale;

      pathParts.push(
         `C ${controlPoint1X} ${controlPoint1Y} ${controlPoint2X} ${controlPoint2Y} ${next.x} ${next.y}`
      );
   }

   return pathParts.join(' ');
}

export function buildExactPathD(points) {
   if (points.length < 2) {
      return '';
   }

   const pathParts = [`M ${points[0].x} ${points[0].y}`];

   for (let index = 1; index < points.length; index += 1) {
      pathParts.push(`L ${points[index].x} ${points[index].y}`);
   }

   return pathParts.join(' ');
}

export function buildRouteMapPoints(points = [], {
   withEntranceLandmark = () => false,
   pointToMapPx = (point) => point,
} = {}) {
   const normalizedPoints = withEntranceLandmark(points)
      .map(pointToMapPx)
      .filter(Boolean);

   if (normalizedPoints.length < 2) {
      return [];
   }

   return normalizedPoints;
}

export function buildItineraryPathD(routePoints, segments = undefined) {
   if (routePoints.length < 2) {
      return '';
   }

   const walkGraphSegments = (
      segments === undefined
         ? getWalkGraphPathSegments()
         : segments
   );
   const walkGraphPathD = walkGraphSegments?.length
      ? buildPathDFromWalkGraphSegments(walkGraphSegments, routePoints)
      : '';

   if (walkGraphPathD) {
      return walkGraphPathD;
   }

   return buildSmoothedPathD(routePoints);
}

export function inclusivePointSlicesForWalkRouteLegs(legs) {
   const slices = [];

   for (let legIndex = 0; legIndex < legs.length; legIndex += 1) {
      const leg = legs[legIndex];
      let fromPointSequence;

      if (slices.length === 0) {
         fromPointSequence = 0;
      } else if (legsShareJoinNode(legs[legIndex - 1], leg)) {
         fromPointSequence = slices[slices.length - 1][1];
      } else {
         fromPointSequence = slices[slices.length - 1][1] + 1;
      }

      const toPointSequence = fromPointSequence + leg.nodeIds.length - 1;
      slices.push([fromPointSequence, toPointSequence]);
   }

   return slices;
}

function legsShareJoinNode(previousLeg, currentLeg) {
   return (
      previousLeg.nodeIds[previousLeg.nodeIds.length - 1]
      === currentLeg.nodeIds[0]
   );
}

export function buildItineraryPathDFromWalkLegs(
   legs,
   points,
   {
      pointToMapPx = (point) => point,
   } = {}
) {
   if (!legs.length) {
      return '';
   }

   const pathParts = [];

   for (const [fromPointSequence, toPointSequence] of inclusivePointSlicesForWalkRouteLegs(legs)) {
      if (toPointSequence >= points.length) {
         continue;
      }

      const routePoints = [];

      for (
         let pointIndex = fromPointSequence;
         pointIndex <= toPointSequence;
         pointIndex += 1
      ) {
         const mappedPoint = pointToMapPx(points[pointIndex]);

         if (!mappedPoint) {
            routePoints.length = 0;
            break;
         }

         routePoints.push(mappedPoint);
      }

      if (routePoints.length < 2) {
         continue;
      }

      // Follow the backend walk-leg waypoints directly. Ride gaps are separate
      // legs, so the next subpath starts at the offboarding station.
      const legPathD = buildSmoothedPathD(routePoints);

      if (legPathD) {
         pathParts.push(legPathD);
      }
   }

   return pathParts.join(' ');
}
