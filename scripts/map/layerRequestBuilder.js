import { ValueNormalizer } from '../api/valueNormalizer.js';
import { TransportationSelectorModel } from '../itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { SourceHelper } from './sourceHelper.js';

export class LayerRequestBuilder {
   static uniqStrings(values) {
      return Array.from(
         new Set(
            (values || [])
               .map(ValueNormalizer.asTrimmedString)
               .filter(Boolean)
         )
      );
   }

   static buildFocusIncludes(focusType, focusRow) {
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
         const species = ValueNormalizer.asTrimmedString(focusRow.species);

         if (species) {
            includes.speciesToInclude = LayerRequestBuilder.uniqStrings([species]);
         }
      }

      if (focusType === 'restaurant' && focusRow.name != null) {
         includes.restaurantsToInclude = LayerRequestBuilder.uniqStrings([focusRow.name]);
      }

      if (focusType === 'giftShop' && focusRow.name != null) {
         includes.giftShopsToInclude = LayerRequestBuilder.uniqStrings([focusRow.name]);
      }

      if (focusType === 'attraction' && focusRow.name != null) {
         includes.attractionsToInclude = LayerRequestBuilder.uniqStrings([focusRow.name]);
      }

      if (focusType === 'transportationStation' && focusRow.name != null) {
         includes.transportationStationsToInclude = LayerRequestBuilder.uniqStrings([focusRow.name]);
      }

      return includes;
   }

   static transportationNamesWithStations(transportationStations) {
      return new Set(
         LayerRequestBuilder.uniqStrings((transportationStations || []).map((station) => station.transportation))
      );
   }

   static isFullyUnscheduledTransportationName(
      name,
      transportations,
      scheduledTransportationNames
   ) {
      if (scheduledTransportationNames.has(name)) {
         return false;
      }

      const rows = (transportations || []).filter(
         (transportation) => TransportationSelectorModel.getTransportationName(transportation) === name
      );

      if (rows.length === 0) {
         return false;
      }

      return rows.every((transportation) => !TransportationSelectorModel.isTransportationScheduled(transportation));
   }

   static buildFullyUnscheduledTransportationRows(
      transportations,
      transportationStations
   ) {
      const scheduledTransportationNames = LayerRequestBuilder.transportationNamesWithStations(
         transportationStations
      );
      const seenNames = new Set();
      const rows = [];

      (transportations || []).forEach((transportation) => {
         const name = TransportationSelectorModel.getTransportationName(transportation);

         if (!name || seenNames.has(name)) {
            return;
         }

         if (!LayerRequestBuilder.isFullyUnscheduledTransportationName(
            name,
            transportations,
            scheduledTransportationNames
         )) {
            return;
         }

         seenNames.add(name);
         rows.push(transportation);
      });

      return SourceHelper.normalizeTypedRows(rows, 'transportation');
   }
}
