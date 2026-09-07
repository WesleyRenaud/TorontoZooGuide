export class RegionSelectionNormalizer {
   static normalizeRegionName(name = '') {
      return typeof name === 'string'
         ? name.trim()
         : '';
   }

   static normalizeRegionExhibits(exhibits = []) {
      return exhibits
         .map((exhibit) => RegionSelectionNormalizer.normalizeRegionName(exhibit))
         .filter(Boolean);
   }
}
