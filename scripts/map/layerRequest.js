import { LayerRequestBuilder } from './layerRequestBuilder.js';
import { MapItemType } from '../shared/enums/mapItemType.js';
import { SourceHelpers } from './sourceHelpers.js';

export class LayerRequest {
   static buildItineraryRows(itinerary) {
      const transportationStations = itinerary?.transportationStations;

      return [
         ...SourceHelpers.normalizeTypedRows(itinerary?.animals, 'animal'),
         ...SourceHelpers.normalizeTypedRows(itinerary?.attractions, 'attraction'),
         ...LayerRequestBuilder.buildFullyUnscheduledTransportationRows(
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
      const normalizedTypes = LayerRequestBuilder.uniqStrings(selectedTypes);
      const routeActive = transportationRoute !== 'none';
      const focusIsTransportationStation = focusType === 'transportationStation';

      if (
         focusType &&
         !normalizedTypes.includes(focusType) &&
         !(routeActive && focusIsTransportationStation && normalizedTypes.includes('transportationRoute'))
      ) {
         return LayerRequestBuilder.uniqStrings([focusType, ...normalizedTypes]);
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
      const includes = LayerRequestBuilder.buildFocusIncludes(focusType, focusRow);

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
