export function filterSpeciesMatches(speciesList, query, maxResults = 12) {
   const normalizedQuery = String(query || '').trim().toLowerCase();

   if (!normalizedQuery) {
      return [];
   }

   const startsWithMatches = [];
   const containsMatches = [];

   speciesList.forEach((species) => {
      const lower = species.toLowerCase();

      if (lower.startsWith(normalizedQuery)) {
         startsWithMatches.push(species);
      } else if (lower.includes(normalizedQuery)) {
         containsMatches.push(species);
      }
   });

   return [...startsWithMatches, ...containsMatches].slice(0, maxResults);
}
