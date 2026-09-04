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

export class SvgPathParsing {
   static pointsNear(left, right, tolerance = 1.5) {
      return Math.hypot(left.x - right.x, left.y - right.y) <= tolerance;
   }

   static parseSvgPathD(pathD) {
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
               controlPoint1X,
               controlPoint1Y,
               controlPoint2X,
               controlPoint2Y,
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
}
