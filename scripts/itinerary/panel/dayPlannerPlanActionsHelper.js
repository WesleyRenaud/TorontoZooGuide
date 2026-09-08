export class DayPlannerPlanActionsHelper {
   static itemHasScheduleTimes(item) {
      return Boolean(String(item?.start_time ?? '').trim())
         && Boolean(String(item?.end_time ?? '').trim());
   }

   static collectionHasScheduledItems(items) {
      return Array.isArray(items)
         && items.some(DayPlannerPlanActionsHelper.itemHasScheduleTimes);
   }
}
