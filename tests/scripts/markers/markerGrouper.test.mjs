import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerGrouper } from '../../../scripts/markers/markerGrouper.js';

test('Test_GroupMarkersByCoordinate_TestItems_ExpectGrouped', () => {
   const groups = MarkerGrouper.groupMarkersByCoordinate([
      { id: 'a', x_coord: 10, y_coord: 20 },
      { id: 'b', x_coord: 10, y_coord: 20 },
      { id: 'c', x_coord: 30, y_coord: 40 },
      { id: 'd', x_coord: null, y_coord: 1 },
   ]);

   assert.equal(groups.size, 2);
   const first = [...groups.values()].find((group) => group.x === 10);
   assert.equal(first.items.length, 2);
   assert.equal(first.items[0].id, 'a');
});

test('Test_GroupMarkersByCoordinate_TestInvalidCoordKey_ExpectSkipped', async () => {
   const { CoordKey } = await import('../../../scripts/map/coordKey.js');
   const original = CoordKey.coordKey;
   CoordKey.coordKey = () => '';

   try {
      const groups = MarkerGrouper.groupMarkersByCoordinate([
         { id: 'a', x_coord: 10, y_coord: 20 },
      ]);
      assert.equal(groups.size, 0);
   } finally {
      CoordKey.coordKey = original;
   }
});
