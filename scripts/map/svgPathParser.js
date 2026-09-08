import { SvgPathParsingHelper } from './svgPathParsingHelper.js';

export class SvgPathParser {
   static TOKEN_PATTERN = /[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?/g;

   static COMMAND_ARG_COUNTS = {
      M: 2,
      L: 2,
      H: 1,
      V: 1,
      C: 6,
      Z: 0,
   };

   static pointsNear(left, right, tolerance = 1.5) {
      return Math.hypot(left.x - right.x, left.y - right.y) <= tolerance;
   }

   static parseSvgPathD(pathD) {
      const tokens = pathD.match(SvgPathParser.TOKEN_PATTERN) ?? [];
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
            x = SvgPathParsingHelper.readNumber(tokens, index);
            y = SvgPathParsingHelper.readNumber(tokens, index + 1);
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
            x = SvgPathParsingHelper.readNumber(tokens, index);
            y = SvgPathParsingHelper.readNumber(tokens, index + 1);
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
            x = SvgPathParsingHelper.readNumber(tokens, index);
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
            y = SvgPathParsingHelper.readNumber(tokens, index);
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
            const controlPoint1X = SvgPathParsingHelper.readNumber(tokens, index);
            const controlPoint1Y = SvgPathParsingHelper.readNumber(tokens, index + 1);
            const controlPoint2X = SvgPathParsingHelper.readNumber(tokens, index + 2);
            const controlPoint2Y = SvgPathParsingHelper.readNumber(tokens, index + 3);
            x = SvgPathParsingHelper.readNumber(tokens, index + 4);
            y = SvgPathParsingHelper.readNumber(tokens, index + 5);
            index += 6;
            segments.push({
               tag: 'C',
               x,
               y,
               controlPoint1X,
               controlPoint1Y,
               controlPoint2X,
               controlPoint2Y,
               d: `C ${controlPoint1X} ${controlPoint1Y} ${controlPoint2X} ${controlPoint2Y} ${x} ${y}`,
            });
            continue;
         }

         if (upperCommand === 'Z') {
            index += SvgPathParser.COMMAND_ARG_COUNTS.Z;
            continue;
         }

         index += SvgPathParser.COMMAND_ARG_COUNTS[upperCommand] ?? 0;
      }

      return segments;
   }
}
