import { SvgPathParser } from './svgPathParser.js';

export class WalkGraphPathGeometryHelper {
   static findSliceBetweenPoints(segments, fromPoint, toPoint, searchStartIndex = 0) {
      const fromIndices = segments
         .map((segment, segmentIndex) => (
            segmentIndex >= searchStartIndex && SvgPathParser.pointsNear(segment, fromPoint)
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

            if (SvgPathParser.pointsNear(segments[toIndex], toPoint)) {
               return {
                  fromIndex,
                  toIndex,
               };
            }
         }
      }

      return null;
   }

   static appendSlice(pathParts, segments, fromIndex, toIndex, includeMove) {
      for (let index = fromIndex; index <= toIndex; index += 1) {
         const segment = segments[index];

         if (segment.tag === 'M' && !includeMove) {
            continue;
         }

         pathParts.push(segment.d);
      }
   }
}
