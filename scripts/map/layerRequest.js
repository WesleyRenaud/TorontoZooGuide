import { isTransportationScheduled } from '../itinerary/selectors/transportationSelector/model.js';
import { MapItemType } from '../shared/enums/mapItemType.js';
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
      ...normalizeTypedRows(itinerary?.transportations, 'transportation')
         .filter((transportation) => !isTransportationScheduled(transportation)),
      ...normalizeTypedRows(itinerary?.guardiansTalks, 'guardiansTalk'),
      ...normalizeTypedRows(itinerary?.wildEncounters, 'wildEncounter'),
      ...normalizeTypedRows(
         itinerary?.transportationStations,
         MapItemType.TRANSPORTATION_STATION
      ),
   ];
}

export function resolveItineraryTransportationRouteMarkers(itinerary) {
   const transportation = itinerary?.transportations?.find((row) => (
      row.route && row.route_markers.length > 0
   ));

   if (!transportation) {
      return null;
   }

   return {
      route: transportation.route,
      markerIds: transportation.route_markers,
   };
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
