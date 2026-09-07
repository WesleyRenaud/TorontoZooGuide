export class RowBuildersHelpers {
   static normalizeItems(items = [], normalizeItem) {
      return items.map((item) => normalizeItem(item));
   }

   static maxStoredLikelihood(...values) {
      const likelihoods = values
         .map((value) => (
            value == null || value === '' ? NaN : Number(value)
         ))
         .filter((value) => Number.isFinite(value));

      if (!likelihoods.length) {
         return null;
      }

      return Math.max(...likelihoods);
   }
}
