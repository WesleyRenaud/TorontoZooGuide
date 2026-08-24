import {
   getTransportationName,
   isTransportationScheduled,
} from '../itinerary/selectors/transportationSelector/model.js';
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

function transportationNamesWithStations(transportationStations) {
   return new Set(
      uniqStrings((transportationStations || []).map((station) => station.transportation))
   );
}

function isFullyUnscheduledTransportationName(
      name,
      transportations,
      scheduledTransportationNames
) {
   if (scheduledTransportationNames.has(name)) {
      return false;
   }

   const rows = (transportations || []).filter(
      (transportation) => getTransportationName(transportation) === name
   );

   if (rows.length === 0) {
      return false;
   }

   return rows.every((transportation) => !isTransportationScheduled(transportation));
}

function buildFullyUnscheduledTransportationRows(
      transportations,
      transportationStations
) {
   const scheduledTransportationNames = transportationNamesWithStations(
      transportationStations
   );
   const seenNames = new Set();
   const rows = [];

   (transportations || []).forEach((transportation) => {
      const name = getTransportationName(transportation);

      if (!name || seenNames.has(name)) {
         return;
      }

      if (!isFullyUnscheduledTransportationName(
         name,
         transportations,
         scheduledTransportationNames
      )) {
         return;
      }

      seenNames.add(name);
      rows.push(transportation);
   });

   return normalizeTypedRows(rows, 'transportation');
}

export function buildItineraryRows(itinerary) {
   const transportationStations = itinerary?.transportationStations;

   return [
      ...normalizeTypedRows(itinerary?.animals, 'animal'),
      ...normalizeTypedRows(itinerary?.attractions, 'attraction'),
      ...buildFullyUnscheduledTransportationRows(
         itinerary?.transportations,
         transportationStations
      ),
      ...normalizeTypedRows(itinerary?.guardiansTalks, 'guardiansTalk'),
      ...normalizeTypedRows(itinerary?.wildEncounters, 'wildEncounter'),
      ...normalizeTypedRows(
         transportationStations,
         MapItemType.TRANSPORTATION_STATION
      ),
   ];
}

export function resolveItineraryTransportationRouteMarkers(itinerary) {
   const transportation = itinerary?.transportations?.find((row) => (
      row.route && row.route_marker_sequences.length > 0
   ));

   if (!transportation) {
      return null;
   }

   return {
      route: transportation.route,
      markerSequences: transportation.route_marker_sequences,
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
