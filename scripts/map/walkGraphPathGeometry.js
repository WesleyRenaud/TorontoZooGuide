import { SvgPathParsing } from './svgPathParsing.js';
import { WalkGraphPathGeometryHelpers } from './walkGraphPathGeometryHelpers.js';

export class WalkGraphPathGeometry {
   static cachedWalkGraphPath = null;

   static getWalkGraphPathSegments() {
      const pathElement = document.querySelector('#walk-graph-path');
      const pathD = pathElement?.getAttribute('d');

      if (!pathD) {
         return null;
      }

      if (WalkGraphPathGeometry.cachedWalkGraphPath?.pathD !== pathD) {
         WalkGraphPathGeometry.cachedWalkGraphPath = {
            pathD,
            segments: SvgPathParsing.parseSvgPathD(pathD),
         };
      }

      return WalkGraphPathGeometry.cachedWalkGraphPath.segments;
   }

   static resetWalkGraphPathCache() {
      WalkGraphPathGeometry.cachedWalkGraphPath = null;
   }

   static buildPathDFromWalkGraphSegments(segments, waypoints) {
      if (!segments.length || waypoints.length < 2) {
         return '';
      }

      const pathParts = [];
      let searchStartIndex = 0;
      let matchedSliceCount = 0;

      for (let index = 0; index < waypoints.length - 1; index += 1) {
         const fromPoint = waypoints[index];
         const toPoint = waypoints[index + 1];
         const slice = WalkGraphPathGeometryHelpers.findSliceBetweenPoints(
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

         WalkGraphPathGeometryHelpers.appendSlice(
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
}
