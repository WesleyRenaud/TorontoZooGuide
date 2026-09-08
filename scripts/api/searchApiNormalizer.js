import { GuardiansTalkLinkedAnimalNormalizer } from '../guardians/guardiansTalkLinkedAnimalNormalizer.js';
import { SearchClient } from './searchClient.js';
import { ValueNormalizer } from './valueNormalizer.js';

export class SearchApiNormalizer {
   static normalizeAttractionRow(row) {
      const source = ValueNormalizer.asObject(row);

      return {
         ...source,
         name: ValueNormalizer.asTrimmedString(source.name),
         free_with_admission: ValueNormalizer.asBoolean(source.free_with_admission),
         part_of_seasonal_attraction: ValueNormalizer.asBoolean(source.part_of_seasonal_attraction),
         is_closed: ValueNormalizer.asBoolean(source.is_closed),
         is_also_transportation: ValueNormalizer.asBoolean(source.is_also_transportation),
         route_duration_minutes: ValueNormalizer.normalizeNumber(source.route_duration_minutes),
         info_link: ValueNormalizer.asNullableString(source.info_link),
         open_time: ValueNormalizer.asNullableString(source.open_time),
         close_time: ValueNormalizer.asNullableString(source.close_time),
      };
   }

   static normalizeGuardiansTalkRow(row) {
      const source = ValueNormalizer.asObject(row);

      return {
         ...source,
         name: ValueNormalizer.asTrimmedString(source.name),
         location: ValueNormalizer.asTrimmedString(source.location),
         start_time: ValueNormalizer.asTrimmedString(source.start_time),
         linked_animals: GuardiansTalkLinkedAnimalNormalizer.normalizeGuardiansTalkLinkedAnimals(source.linked_animals),
      };
   }

   static normalizeWildEncounterRow(row) {
      const source = ValueNormalizer.asObject(row);

      return {
         ...source,
         name: ValueNormalizer.asTrimmedString(source.name),
         meeting_spot: ValueNormalizer.asTrimmedString(source.meeting_spot),
         start_time: ValueNormalizer.asTrimmedString(source.start_time),
         link: ValueNormalizer.asNullableString(source.link),
      };
   }

   static normalizeTransportationRow(row) {
      const source = ValueNormalizer.asObject(row);

      return {
         ...source,
         name: ValueNormalizer.asTrimmedString(source.name),
         free_with_admission: ValueNormalizer.asBoolean(source.free_with_admission),
         is_also_attraction: ValueNormalizer.asBoolean(source.is_also_attraction),
         info_link: ValueNormalizer.asNullableString(source.info_link),
         open_time: ValueNormalizer.asNullableString(source.open_time),
         close_time: ValueNormalizer.asNullableString(source.close_time),
      };
   }

   static normalizeSearchEndpointResponse(endpoint, response) {
      if (endpoint === '/search') {
         return SearchClient.normalizeSearchResponse(response);
      }

      return response;
   }
}
