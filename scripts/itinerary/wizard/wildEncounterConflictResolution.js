export function getSelectedWildEncounters(conflictGroups = []) {
   const selectedEncounters = conflictGroups
      .map((group) => group?.selection?.item)
      .filter(Boolean);
   const seenNames = new Set();

   return selectedEncounters.filter((encounter) => {
      if (seenNames.has(encounter.name)) {
         return false;
      }

      seenNames.add(encounter.name);
      return true;
   });
}

export function hasWildEncounterConflictSelection(conflictGroups = []) {
   return getSelectedWildEncounters(conflictGroups).length > 0;
}

export function buildItineraryWithSelectedWildEncounters(
   itinerary,
   wildEncounters = [],
) {
   return {
      ...itinerary,
      wildEncounters: [
         ...itinerary.wildEncounters,
         ...wildEncounters,
      ],
   };
}
