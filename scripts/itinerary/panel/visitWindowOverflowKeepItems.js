import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';

export class VisitWindowOverflowKeepItems {
   static overflowItemsFromIssues(issues) {
      return issues.flatMap((issue) => {
         if (issue.type !== ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS) {
            return [];
         }

         return issue.items;
      });
   }


   static itemKey(item) {
      return `${item.name}::${item.item_type}::${item.start_time}`;
   }


   static createKeptItemKeys(items) {
      return new Set(items.map((item) => VisitWindowOverflowKeepItems.itemKey(item)));
   }


   static isKept(keptItemKeys, item) {
      return keptItemKeys.has(VisitWindowOverflowKeepItems.itemKey(item));
   }


   static toggleKeep(keptItemKeys, item) {
      const key = VisitWindowOverflowKeepItems.itemKey(item);

      if (keptItemKeys.has(key)) {
         keptItemKeys.delete(key);
         return;
      }

      keptItemKeys.add(key);
   }


   static toKeepWire(item) {
      const keepItem = {
         name: item.name,
         item_type: item.item_type,
      };

      if (item.start_time) {
         keepItem.start_time = item.start_time;
      }

      return keepItem;
   }


   static keptWiresFromKeys(items, keptItemKeys) {
      return items
         .filter((item) => VisitWindowOverflowKeepItems.isKept(keptItemKeys, item))
         .map((item) => VisitWindowOverflowKeepItems.toKeepWire(item));
   }
}
