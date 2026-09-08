import { ItemView } from './itemView.js';
import { RemovedItemsPopupAdjustmentBuilder } from './removedItemsPopupAdjustmentBuilder.js';

export class RemovedItemsPopupContentRowsBuilder {
   static buildAdjustmentRows(adjustments = []) {
      return adjustments.map((adjustment) => {
         const rowSpec = RemovedItemsPopupAdjustmentBuilder.buildAdjustmentRowSpec(adjustment);

         if (!rowSpec) {
            return null;
         }

         return ItemView.makeItemRow(rowSpec);
      });
   }
}
