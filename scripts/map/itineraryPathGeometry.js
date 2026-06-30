const TOKEN_PATTERN = /[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?/g;

const COMMAND_ARG_COUNTS = {
   M: 2,
   L: 2,
   H: 1,
   V: 1,
   C: 6,
   Z: 0,
};

function readNumber(tokens, index) {
   return Number.parseFloat(tokens[index]);
}

function pointsNear(left, right, tolerance = 1.5) {
   return Math.hypot(left.x - right.x, left.y - right.y) <= tolerance;
}

export function parseSvgPathD(pathD) {
   const tokens = pathD.match(TOKEN_PATTERN) ?? [];
   const segments = [];
   let index = 0;
   let command = '';
   let x = 0;
   let y = 0;

   while (index < tokens.length) {
      if (/[a-zA-Z]/.test(tokens[index])) {
         command = tokens[index];
         index += 1;
      }
      else if (!command) {
         index += 1;
         continue;
      }

      const upperCommand = command.toUpperCase();

      if (upperCommand === 'M') {
         x = readNumber(tokens, index);
         y = readNumber(tokens, index + 1);
         index += 2;
         segments.push({
            tag: 'M',
            x,
            y,
            d: `M ${x} ${y}`,
         });
         command = 'L';
         continue;
      }

      if (upperCommand === 'L') {
         x = readNumber(tokens, index);
         y = readNumber(tokens, index + 1);
         index += 2;
         segments.push({
            tag: 'L',
            x,
            y,
            d: `L ${x} ${y}`,
         });
         continue;
      }

      if (upperCommand === 'H') {
         x = readNumber(tokens, index);
         index += 1;
         segments.push({
            tag: 'H',
            x,
            y,
            d: `L ${x} ${y}`,
         });
         continue;
      }

      if (upperCommand === 'V') {
         y = readNumber(tokens, index);
         index += 1;
         segments.push({
            tag: 'V',
            x,
            y,
            d: `L ${x} ${y}`,
         });
         continue;
      }

      if (upperCommand === 'C') {
         const controlPoint1X = readNumber(tokens, index);
         const controlPoint1Y = readNumber(tokens, index + 1);
         const controlPoint2X = readNumber(tokens, index + 2);
         const controlPoint2Y = readNumber(tokens, index + 3);
         x = readNumber(tokens, index + 4);
         y = readNumber(tokens, index + 5);
         index += 6;
         segments.push({
            tag: 'C',
            x,
            y,
            d: `C ${controlPoint1X} ${controlPoint1Y} ${controlPoint2X} ${controlPoint2Y} ${x} ${y}`,
         });
         continue;
      }

      if (upperCommand === 'Z') {
         index += COMMAND_ARG_COUNTS.Z;
         continue;
      }

      index += COMMAND_ARG_COUNTS[upperCommand] ?? 0;
   }

   return segments;
}

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
            pathParts.push(`M ${fromPoint.x} ${fromPoint.y} L ${toPoint.x} ${toPoint.y}`);
         }
         else {
            pathParts.push(`L ${toPoint.x} ${toPoint.y}`);
         }

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

let cachedWalkGraphPath = null;

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

export function buildItineraryPathD(routePoints, segments = null) {
   if (routePoints.length < 2) {
      return '';
   }

   const walkGraphSegments = segments ?? getWalkGraphPathSegments();
   const walkGraphPathD = walkGraphSegments
      ? buildPathDFromWalkGraphSegments(walkGraphSegments, routePoints)
      : '';

   if (walkGraphPathD) {
      return walkGraphPathD;
   }

   return buildSmoothedPathD(routePoints);
}
