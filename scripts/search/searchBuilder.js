import { ItemType } from '../shared/enums/itemType.js';
import { ScheduleItemKind } from '../shared/enums/scheduleItemKind.js';

export class SearchBuilder {
   static SEARCH_GROUPS = [
      [ScheduleItemKind.ANIMAL.itemType, ItemType.ANIMAL],
      ['pavilions', ItemType.PAVILION],
      ['restaurants', ItemType.RESTAURANT],
      ['restrooms', ItemType.RESTROOM],
      ['gift_shops', ItemType.GIFT_SHOP],
      [ScheduleItemKind.ATTRACTION.itemType, ItemType.ATTRACTION],
      ['transportation_stations', ItemType.TRANSPORTATION_STATION],
      [ScheduleItemKind.GUARDIANS_TALK.itemType, ItemType.GUARDIANS_TALK],
      [ScheduleItemKind.WILD_ENCOUNTER.itemType, ItemType.WILD_ENCOUNTER],
   ];

   static flattenSearchRows(response) {
      return SearchBuilder.SEARCH_GROUPS.flatMap(([key, type]) => {
         const rows = Array.isArray(response?.[key]) ? response[key] : [];

         return rows.map((row) => ({
            ...row,
            type,
         }));
      });
   }
}
