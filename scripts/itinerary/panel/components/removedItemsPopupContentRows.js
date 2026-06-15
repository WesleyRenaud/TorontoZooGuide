import { makeItemRow } from './itemRow.js';
import { buildAdjustmentRowSpec } from './removedItemsPopupAdjustmentSpecs.js';

export function buildAdjustmentRows(adjustments = []) {
   return adjustments.map((adjustment) => {
      const rowSpec = buildAdjustmentRowSpec(adjustment);

      if (!rowSpec) {
         return null;
      }

      return makeItemRow(rowSpec);
   });
}
