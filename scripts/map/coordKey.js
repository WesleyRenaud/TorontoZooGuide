export class CoordKey {
   static coordKey(x, y) {
      const normalizedX = Number(x);
      const normalizedY = Number(y);

      return `${normalizedX.toFixed(4)}|${normalizedY.toFixed(4)}`;
   }
}
