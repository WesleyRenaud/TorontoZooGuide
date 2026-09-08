import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { StoredSelection } from '../base/storedSelection.js';
import { ItineraryTransportationStationRoles } from '../../itineraryTransportationStationRoles.js';
import { TransportationSelectorModel } from './transportationSelectorModel.js';

export class TransportationStationNameResolver {
   static asObject(value) {
      return value && typeof value === 'object'
         ? value
         : {};
   }

   static uniqueNames(names) {
      const seen = new Set();
      const ordered = [];

      names.forEach((name) => {
         if (!name || seen.has(name)) {
            return;
         }

         seen.add(name);
         ordered.push(name);
      });

      return ordered;
   }

   static namesForRoles(stations, roles) {
      return TransportationStationNameResolver.uniqueNames(
         stations
            .filter((station) => roles.includes(station.role))
            .map((station) => ValueNormalizer.asTrimmedString(station.name))
      );
   }

   static getTransportationLegs(row) {
      const legs = TransportationStationNameResolver.asObject(row).legs;

      return Array.isArray(legs)
         ? legs.map((leg) => TransportationStationNameResolver.asObject(leg))
         : [];
   }

   static fallbackStationNames(row, pickFromLeg) {
      const legs = TransportationStationNameResolver.getTransportationLegs(row);

      if (legs.length > 0) {
         const name = ValueNormalizer.asTrimmedString(pickFromLeg(legs));
         return name ? [name] : [];
      }

      if (!TransportationSelectorModel.isTransportationAddedAsAttraction(row)) {
         return [];
      }

      const mainStation = ValueNormalizer.asTrimmedString(row?.main_station);
      return mainStation ? [mainStation] : [];
   }

   static boardingStationNames(row) {
      const stations = TransportationSelectorModel.getTransportationStations(row);

      if (stations.length > 0) {
         return TransportationStationNameResolver.namesForRoles(
            stations,
            ItineraryTransportationStationRoles.getItineraryTransportationStationOnboardingRoles()
         );
      }

      return TransportationStationNameResolver.fallbackStationNames(row, (legs) => legs[0].from_station);
   }

   static offboardingStationNames(row) {
      const stations = TransportationSelectorModel.getTransportationStations(row);

      if (stations.length > 0) {
         return TransportationStationNameResolver.namesForRoles(
            stations,
            ItineraryTransportationStationRoles.getItineraryTransportationStationOffboardingRoles()
         );
      }

      return TransportationStationNameResolver.fallbackStationNames(row, (legs) => legs[legs.length - 1].to_station);
   }

   static createStoredTransportationFromString(item) {
      const name = ValueNormalizer.asTrimmedString(item);

      if (!name) {
         return null;
      }

      return {
         id: name,
         name,
         subtitle: '',
         infoLink: null,
         imageSrc: null,
         addedAsAttraction: false,
      };
   }

   static createStoredTransportationFromObject(item) {
      const name = ValueNormalizer.asTrimmedString(item.name);
      const id = StoredSelection.normalizeStoredId(item.id, name);

      if (!id) {
         return null;
      }

      return {
         id,
         name,
         subtitle: ValueNormalizer.asTrimmedString(item.subtitle),
         infoLink: StoredSelection.normalizeStoredLink(item.infoLink),
         imageSrc: StoredSelection.normalizeStoredLink(item.imageSrc),
         addedAsAttraction: StoredSelection.normalizeStoredBoolean(item.addedAsAttraction),
      };
   }
}
