import assert from 'node:assert/strict';
import test from 'node:test';

import { ItemView } from '../../../../../scripts/itinerary/panel/components/itemView.js';
import { RemovedItemsPopupAdjustmentBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupAdjustmentBuilder.js';
import { RemovedItemsPopupContentRowsBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupContentRowsBuilder.js';

test('Test_BuildAdjustmentRows_TestSpecs_ExpectRowsOrNull', () => {
   const originalSpec = RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec;
   const originalRow = ItemView.makeItemRow;
   RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec = (adjustment) => (
      adjustment.ok ? { name: adjustment.name } : null
   );
   ItemView.makeItemRow = (spec) => ({ row: spec.name });

   try {
      assert.deepEqual(
         RemovedItemsPopupContentRowsBuilder.buildAdjustmentRows([
            { ok: true, name: 'A' },
            { ok: false, name: 'B' },
         ]),
         [{ row: 'A' }, null]
      );
   } finally {
      RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec = originalSpec;
      ItemView.makeItemRow = originalRow;
   }
});
