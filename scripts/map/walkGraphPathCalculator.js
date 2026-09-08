import { SvgPathParser } from './svgPathParser.js';
import { WalkGraphPathGeometryHelper } from './walkGraphPathGeometryHelper.js';

export class WalkGraphPathCalculator {
   static cachedWalkGraphPath = null;

   static getWalkGraphPathSegments() {
      const pathElement = document.querySelector('#walk-graph-path');
      const pathD = pathElement?.getAttribute('d');

      if (!pathD) {
         return null;
      }

      if (WalkGraphPathCalculator.cachedWalkGraphPath?.pathD !== pathD) {
         WalkGraphPathCalculator.cachedWalkGraphPath = {
            pathD,
            segments: SvgPathParser.parseSvgPathD(pathD),
         };
      }

      return WalkGraphPathCalculator.cachedWalkGraphPath.segments;
   }

   static resetWalkGraphPathCache() {
      WalkGraphPathCalculator.cachedWalkGraphPath = null;
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
         const slice = WalkGraphPathGeometryHelper.findSliceBetweenPoints(
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

         WalkGraphPathGeometryHelper.appendSlice(
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
