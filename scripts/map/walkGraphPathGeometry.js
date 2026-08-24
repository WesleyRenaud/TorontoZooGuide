import {
   parseSvgPathD,
   pointsNear,
} from './svgPathParsing.js';

let cachedWalkGraphPath = null;

function findSliceBetweenPoints(segments, fromPoint, toPoint, searchStartIndex = 0) {
   const fromIndices = segments
      .map((segment, segmentIndex) => (
         segmentIndex >= searchStartIndex && pointsNear(segment, fromPoint)
            ? segmentIndex
            : -1
      ))
      .filter((segmentIndex) => segmentIndex >= 0);

   for (const fromIndex of fromIndices) {
      for (
         let toIndex = fromIndex + 1;
         toIndex < segments.length;
         toIndex += 1
      ) {
         if (segments[toIndex].tag === 'M') {
            break;
         }

         if (pointsNear(segments[toIndex], toPoint)) {
            return {
               fromIndex,
               toIndex,
            };
         }
      }
   }

   return null;
}

function appendSlice(pathParts, segments, fromIndex, toIndex, includeMove) {
   for (let index = fromIndex; index <= toIndex; index += 1) {
      const segment = segments[index];

      if (segment.tag === 'M' && !includeMove) {
         continue;
      }

      pathParts.push(segment.d);
   }
}

export function getWalkGraphPathSegments() {
   const pathElement = document.querySelector('#walk-graph-path');
   const pathD = pathElement?.getAttribute('d');

   if (!pathD) {
      return null;
   }

   if (cachedWalkGraphPath?.pathD !== pathD) {
      cachedWalkGraphPath = {
         pathD,
         segments: parseSvgPathD(pathD),
      };
   }

   return cachedWalkGraphPath.segments;
}

export function resetWalkGraphPathCache() {
   cachedWalkGraphPath = null;
}

export function buildPathDFromWalkGraphSegments(segments, waypoints) {
   if (!segments.length || waypoints.length < 2) {
      return '';
   }

   const pathParts = [];
   let searchStartIndex = 0;
   let matchedSliceCount = 0;

   for (let index = 0; index < waypoints.length - 1; index += 1) {
      const fromPoint = waypoints[index];
      const toPoint = waypoints[index + 1];
      const slice = findSliceBetweenPoints(
         segments,
         fromPoint,
         toPoint,
         searchStartIndex
      );

      if (!slice) {
         if (matchedSliceCount === 0) {
            pathParts.push(
               `M ${fromPoint.x} ${fromPoint.y} L ${toPoint.x} ${toPoint.y}`
            );
         }
         else {
            pathParts.push(`L ${toPoint.x} ${toPoint.y}`);
         }

         matchedSliceCount += 1;
         continue;
      }

      appendSlice(
         pathParts,
         segments,
         slice.fromIndex,
         slice.toIndex,
         matchedSliceCount === 0
      );
      matchedSliceCount += 1;
      searchStartIndex = slice.toIndex;
   }

   if (pathParts.length === 0) {
      return '';
   }

   return pathParts.join(' ');
}
