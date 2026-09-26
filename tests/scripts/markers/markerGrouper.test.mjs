import assert from 'node:assert/strict';
import test from 'node:test';

import { CoordKey } from '../../../scripts/map/coordKey.js';
import { MarkerGrouper } from '../../../scripts/markers/markerGrouper.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_GroupMarkersByCoordinate_TestItems_ExpectGrouped', () => {
   const first = { id: 'a', x_coord: 10, y_coord: 20 };
   const second = { id: 'b', x_coord: first.x_coord, y_coord: first.y_coord };
   const third = { id: 'c', x_coord: 30, y_coord: 40 };
   const items = [
      first,
      second,
      third,
      { id: 'd', x_coord: null, y_coord: 1 },
   ];

   const groups = MarkerGrouper.groupMarkersByCoordinate(items);
   const grouped = [...groups.values()].find((group) => group.x === first.x_coord);

   assert.equal(groups.size, 2);
   assert.equal(grouped.items.length, 2);
   assert.equal(grouped.items.at(Position.FIRST).id, first.id);
});


test('Test_GroupMarkersByCoordinate_TestInvalidCoordKey_ExpectSkipped', () => {
   const original = CoordKey.coordKey;
   CoordKey.coordKey = () => '';

   try {
      const items = [{ id: 'a', x_coord: 10, y_coord: 20 }];

      const groups = MarkerGrouper.groupMarkersByCoordinate(items);

      assert.equal(groups.size, 0);
   } finally {
      CoordKey.coordKey = original;
   }
});
