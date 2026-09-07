import { ApiClient } from './apiClient.js';
import { ValueNormalizer } from './valueNormalizer.js';

const EMPTY_PAYLOAD = Object.freeze({});

export class MapApiFetcher {
   static asStringArray(value) {
      return ValueNormalizer.asArray(value)
         .map(ValueNormalizer.asTrimmedString)
         .filter(Boolean);
   }

   static readResponseCollection(response, responseKey) {
      return ValueNormalizer.asArray(ValueNormalizer.asObject(response)[responseKey]);
   }

   static normalizeRouteResponse(response) {
      const source = ValueNormalizer.asObject(response);

      return {
         route: ValueNormalizer.asTrimmedString(source.route).toLowerCase(),
         transportationStations: MapApiFetcher.readResponseCollection(source, 'transportation_stations'),
      };
   }

   static async fetchCollection(endpoint, responseKey, payload = EMPTY_PAYLOAD) {
      const response = await ApiClient.postJson(endpoint, payload);
      return MapApiFetcher.readResponseCollection(response, responseKey);
   }

   static async fetchStringCollection(endpoint, responseKey, payload = EMPTY_PAYLOAD) {
      return MapApiFetcher.asStringArray(await MapApiFetcher.fetchCollection(endpoint, responseKey, payload));
   }

   static normalizeTransportationRoutesResponse(response) {
      return ValueNormalizer.asArray(ValueNormalizer.asObject(response).transportations)
         .map((entry) => {
            const source = ValueNormalizer.asObject(entry);
            const name = ValueNormalizer.asTrimmedString(source.name);

            if (!name) {
               return null;
            }

            return {
               name,
               routes: MapApiFetcher.asStringArray(source.routes),
            };
         })
         .filter(Boolean);
   }
}
