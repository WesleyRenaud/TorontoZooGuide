import { CoordKey } from '../map/coordKey.js';

export class MarkerGroups {
   static groupMarkersByCoordinate(items) {
      const markerMap = new Map();

      (items || []).forEach((item) => {
         const x = item?.x_coord ?? null;
         const y = item?.y_coord ?? null;

         if (x == null || y == null) {
            return;
         }

         const key = CoordKey.coordKey(x, y);

         if (!key) {
            return;
         }

         if (!markerMap.has(key)) {
            markerMap.set(key, {
               key,
               x: Number(x),
               y: Number(y),
               items: [],
            });
         }

         markerMap.get(key).items.push(item);
      });

      return markerMap;
   }
}
