import assert from 'node:assert/strict';
import test from 'node:test';

import { ItemView } from '../../../../../scripts/itinerary/panel/components/itemView.js';
import { RemovedItemsPopupAdjustmentBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupAdjustmentBuilder.js';
import { RemovedItemsPopupContentRowsBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupContentRowsBuilder.js';


test('Test_BuildAdjustmentRows_TestSpecs_ExpectRowsOrNull', () => {
   const originalSpec = RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec;
   const originalRow = ItemView.makeItemRow;
   const lion = 'African Lion';
   const tiger = 'Amur Tiger';
   const adjustments = [
      { ok: true, name: lion },
      { ok: false, name: tiger },
   ];

   RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec = (adjustment) => (
      adjustment.ok ? { name: adjustment.name } : null
   );
   ItemView.makeItemRow = (spec) => ({ row: spec.name });

   try {
      const rows = RemovedItemsPopupContentRowsBuilder.buildAdjustmentRows(adjustments);

      assert.deepEqual(rows, [{ row: lion }, null]);
   } finally {
      RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec = originalSpec;
      ItemView.makeItemRow = originalRow;
   }
});
