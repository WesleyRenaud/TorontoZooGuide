import { ItemType } from '../shared/enums/itemType.js';

export class SearchBuilder {
   static SEARCH_GROUPS = [
      ['animals', ItemType.ANIMAL],
      ['pavilions', ItemType.PAVILION],
      ['restaurants', ItemType.RESTAURANT],
      ['restrooms', ItemType.RESTROOM],
      ['gift_shops', ItemType.GIFT_SHOP],
      ['attractions', ItemType.ATTRACTION],
      ['transportation_stations', ItemType.TRANSPORTATION_STATION],
      ['guardians_talks', ItemType.GUARDIANS_TALK],
      ['wild_encounters', ItemType.WILD_ENCOUNTER],
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
