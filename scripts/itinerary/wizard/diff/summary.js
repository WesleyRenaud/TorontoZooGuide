function hasItems(items) {
   return Array.isArray(items) && items.length > 0;
}

export function hasRemovedItems(removed) {
   if (!removed || typeof removed !== 'object') {
      return false;
   }

   return (
      hasItems(removed.animals) ||
      hasItems(removed.attractions) ||
      hasItems(removed.guardiansTalks) ||
      hasItems(removed.wildEncounters)
   );
}

export function hasAddedItems(added) {
   if (!added || typeof added !== 'object') {
      return false;
   }

   return hasItems(added.animals);
}

export function hasReducedVisibility(reducedVisibility) {
   if (!reducedVisibility || typeof reducedVisibility !== 'object') {
      return false;
   }

   return hasItems(reducedVisibility.animals);
}

export function hasImprovedVisibility(improvedVisibility) {
   if (!improvedVisibility || typeof improvedVisibility !== 'object') {
      return false;
   }

   return hasItems(improvedVisibility.animals);
}

export function hasUnscheduledItems(unscheduled) {
   if (!unscheduled || typeof unscheduled !== 'object') {
      return false;
   }

   return hasItems(unscheduled.animals) || hasItems(unscheduled.attractions);
}

export function isValidatedItineraryEmpty(validated) {
   if (!validated || typeof validated !== 'object') {
      return true;
   }

   return (
      !hasItems(validated.animals) &&
      !hasItems(validated.attractions) &&
      !hasItems(validated.guardiansTalks) &&
      !hasItems(validated.wildEncounters)
   );
}
