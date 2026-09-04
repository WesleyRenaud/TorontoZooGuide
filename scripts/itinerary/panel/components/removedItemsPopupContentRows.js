import { makeItemRow } from './itemRow.js';
import { RemovedItemsPopupAdjustmentSpecs } from './removedItemsPopupAdjustmentSpecs.js';

export class RemovedItemsPopupContentRows {
   static buildAdjustmentRows(adjustments = []) {
      return adjustments.map((adjustment) => {
         const rowSpec = RemovedItemsPopupAdjustmentSpecs.buildAdjustmentRowSpec(adjustment);

         if (!rowSpec) {
            return null;
         }

         return makeItemRow(rowSpec);
      });
   }
}
