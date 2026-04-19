const SEARCH_GROUPS = [
   ['animals', 'animal'],
   ['pavilions', 'pavilion'],
   ['restaurants', 'restaurant'],
   ['restrooms', 'restroom'],
   ['gift_shops', 'giftShop'],
   ['attractions', 'attraction'],
   ['zoomobile_stations', 'zoomobileStation'],
   ['guardians_talks', 'guardiansTalk'],
   ['wild_encounters', 'wildEncounter'],
];

export function flattenSearchRows(response) {
   return SEARCH_GROUPS.flatMap(([key, type]) => {
      const rows = Array.isArray(response?.[key]) ? response[key] : [];

      return rows.map((row) => ({
         ...row,
         type,
      }));
   });
}
