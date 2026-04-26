import { normalizeTypedRows } from './sourceHelpers.js';

function uniqStrings(values) {
   return Array.from(
      new Set(
         (values || [])
            .map((value) => String(value || '').trim())
            .filter(Boolean)
      )
   );
}

function buildFocusIncludes(focusType, focusRow) {
   const includes = {
      speciesToInclude: [],
      restaurantsToInclude: [],
      giftShopsToInclude: [],
      attractionsToInclude: [],
      zoomobileStationsToInclude: [],
   };

   if (!focusRow) {
      return includes;
   }

   if (focusType === 'animal') {
      const species = String(focusRow.species || '').trim();

      if (species) {
         includes.speciesToInclude = uniqStrings([species]);
      }
   }

   if (focusType === 'restaurant' && focusRow.name != null) {
      includes.restaurantsToInclude = uniqStrings([focusRow.name]);
   }

   if (focusType === 'giftShop' && focusRow.name != null) {
      includes.giftShopsToInclude = uniqStrings([focusRow.name]);
   }

   if (focusType === 'attraction' && focusRow.name != null) {
      includes.attractionsToInclude = uniqStrings([focusRow.name]);
   }

   if (focusType === 'zoomobileStation' && focusRow.name != null) {
      includes.zoomobileStationsToInclude = uniqStrings([focusRow.name]);
   }

   return includes;
}

export function buildItineraryRows(itinerary) {
   return [
      ...normalizeTypedRows(itinerary?.animals, 'animal'),
      ...normalizeTypedRows(itinerary?.attractions, 'attraction'),
      ...normalizeTypedRows(itinerary?.guardiansTalks, 'guardiansTalk'),
      ...normalizeTypedRows(itinerary?.wildEncounters, 'wildEncounter'),
   ];
}

export function buildSelectedTypes(selectedTypes, focusType, zoomobileRoute) {
   const normalizedTypes = uniqStrings(selectedTypes);
   const routeActive = zoomobileRoute !== 'none';
   const focusIsZoomobileStation = focusType === 'zoomobileStation';

   if (
      focusType &&
      !normalizedTypes.includes(focusType) &&
      !(routeActive && focusIsZoomobileStation && normalizedTypes.includes('zoomobileRoute'))
   ) {
      return uniqStrings([focusType, ...normalizedTypes]);
   }

   return normalizedTypes;
}

export function buildLayerRequest({
   dateCtx,
   selectedTypes,
   zoomobileRoute,
   focusRow,
   focusType,
   includeOffDisplayAnimals,
   includeClosedRestaurants,
   includeClosedRestrooms,
   includeClosedGiftShops,
   includeClosedAttractions,
}) {
   const includes = buildFocusIncludes(focusType, focusRow);

   return {
      selectedTypes: buildSelectedTypes(selectedTypes, focusType, zoomobileRoute),
      ctx: {
         month: dateCtx.month,
         day: dateCtx.day,
         dayOfWeek: dateCtx.dayOfWeek ?? 1,
         temp: dateCtx.temp ?? null,
         includeOffDisplayAnimals,
         includeClosedRestaurants,
         includeClosedRestrooms,
         includeClosedGiftShops,
         includeClosedAttractions,
         zoomobileRoute,
         ...includes,
      },
   };
}
