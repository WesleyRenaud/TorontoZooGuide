import {
   getTransportationName,
   isTransportationScheduled,
} from '../itinerary/selectors/transportationSelector/model.js';
import { MapItemType } from '../shared/enums/mapItemType.js';
import { SourceHelpers } from './sourceHelpers.js';

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
      transportationStationsToInclude: [],
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

   if (focusType === 'transportationStation' && focusRow.name != null) {
      includes.transportationStationsToInclude = uniqStrings([focusRow.name]);
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

   return SourceHelpers.normalizeTypedRows(rows, 'transportation');
}

export class LayerRequest {
   static buildItineraryRows(itinerary) {
      const transportationStations = itinerary?.transportationStations;

      return [
         ...SourceHelpers.normalizeTypedRows(itinerary?.animals, 'animal'),
         ...SourceHelpers.normalizeTypedRows(itinerary?.attractions, 'attraction'),
         ...buildFullyUnscheduledTransportationRows(
            itinerary?.transportations,
            transportationStations
         ),
         ...SourceHelpers.normalizeTypedRows(itinerary?.guardiansTalks, 'guardiansTalk'),
         ...SourceHelpers.normalizeTypedRows(itinerary?.wildEncounters, 'wildEncounter'),
         ...SourceHelpers.normalizeTypedRows(
            transportationStations,
            MapItemType.TRANSPORTATION_STATION
         ),
      ];
   }

   static resolveItineraryTransportationRouteMarkers(itinerary) {
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

   static buildSelectedTypes(selectedTypes, focusType, transportationRoute) {
      const normalizedTypes = uniqStrings(selectedTypes);
      const routeActive = transportationRoute !== 'none';
      const focusIsTransportationStation = focusType === 'transportationStation';

      if (
         focusType &&
         !normalizedTypes.includes(focusType) &&
         !(routeActive && focusIsTransportationStation && normalizedTypes.includes('transportationRoute'))
      ) {
         return uniqStrings([focusType, ...normalizedTypes]);
      }

      return normalizedTypes;
   }

   static buildLayerRequest({
      dateCtx,
      selectedTypes,
      transportationRoute,
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
         selectedTypes: LayerRequest.buildSelectedTypes(selectedTypes, focusType, transportationRoute),
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
            transportationRoute,
            ...includes,
         },
      };
   }
}
