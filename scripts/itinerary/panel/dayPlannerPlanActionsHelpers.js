import { ValueNormalizer } from '../../api/valueNormalizer.js';

export class DayPlannerPlanActionsHelpers {
   static itemHasScheduleTimes(item) {
      return Boolean(ValueNormalizer.asTrimmedString(item?.start_time))
         && Boolean(ValueNormalizer.asTrimmedString(item?.end_time));
   }

   static collectionHasScheduledItems(items) {
      return Array.isArray(items)
         && items.some(DayPlannerPlanActionsHelpers.itemHasScheduleTimes);
   }
}
