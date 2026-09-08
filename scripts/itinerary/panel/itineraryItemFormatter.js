import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { GuardiansTalkLinkedAnimalNormalizer } from '../../guardians/guardiansTalkLinkedAnimalNormalizer.js';
import { ItineraryItemFormatterHelper } from './itineraryItemFormatterHelper.js';
import { WildEncounterScheduleItemKey } from '../selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';

export class ItineraryItemFormatter {
   static normalizeNumber = ValueNormalizer.normalizeNumber;

   static normalizeNonNegativeNumber(value) {
      const number = ValueNormalizer.normalizeNumber(value);

      if (number == null || number < 0) {
         return null;
      }

      return number;
   }

   static parseDurationMinutes(value) {
      const normalized = ValueNormalizer.asTrimmedString(value);

      if (!normalized) {
         return null;
      }

      const parsed = Number(normalized);

      if (!Number.isFinite(parsed) || parsed <= 0) {
         return null;
      }

      return Math.round(parsed);
   }

   static formatISODateLong(iso) {
      if (!iso || typeof iso !== 'string') return '';

      const date = new Date(`${iso}T12:00:00`);

      if (!Number.isFinite(date.getTime())) return '';

      return date.toLocaleDateString(undefined, {
         weekday: 'long',
         year: 'numeric',
         month: 'long',
         day: 'numeric',
      });
   }

   static formatISODateFull(iso, fallback = '') {
      if (!iso || typeof iso !== 'string') return fallback;

      const trimmedIso = ValueNormalizer.asTrimmedString(iso);
      const dateParts = trimmedIso.match(/^(\d{4})-(\d{2})-(\d{2})$/);

      if (!dateParts) {
         return trimmedIso || fallback;
      }

      const date = new Date(
         Number(dateParts[1]),
         Number(dateParts[2]) - 1,
         Number(dateParts[3])
      );

      return new Intl.DateTimeFormat('en-CA', {
         weekday: 'long',
         month: 'long',
         day: 'numeric',
         year: 'numeric',
      }).format(date);
   }

   static formatClockTime(timeValue, fallback = '') {
      const trimmedTimeValue = ValueNormalizer.asTrimmedString(timeValue);

      if (!trimmedTimeValue) {
         return fallback;
      }

      const timeParts = trimmedTimeValue.match(/^(\d{1,2}):(\d{2})(?::(\d{2}))?$/);

      if (!timeParts) {
         return trimmedTimeValue;
      }

      const hours = Number(timeParts[1]);
      const minutes = Number(timeParts[2]);
      const seconds = timeParts[3] == null ? 0 : Number(timeParts[3]);
      const period = hours >= 12 ? 'PM' : 'AM';
      const displayHours = hours % 12 || 12;
      const secondsLabel = seconds > 0
         ? `:${String(seconds).padStart(2, '0')}`
         : '';

      return `${displayHours}:${String(minutes).padStart(2, '0')}${secondsLabel} ${period}`;
   }

   static normalizeAnimal(value) {
      const source = ItineraryItemFormatterHelper.asObject(value);

      return {
         ...source,
         species: ValueNormalizer.asTrimmedString(source.species),
         exhibit: ValueNormalizer.asTrimmedString(source.exhibit),
         link: ValueNormalizer.asNullableString(source.link),
         removalReason: ValueNormalizer.asNullableString(source.removalReason),
         likelihoodBefore: ValueNormalizer.normalizeNumber(source.likelihoodBefore),
         likelihoodAfter: ValueNormalizer.normalizeNumber(source.likelihoodAfter),
      };
   }

   static normalizeAttraction(value) {
      const source = ItineraryItemFormatterHelper.asObject(value);

      return {
         ...source,
         name: ValueNormalizer.asTrimmedString(source.name),
         subtitle: ValueNormalizer.asTrimmedString(source.subtitle),
         region: ValueNormalizer.asTrimmedString(source.region),
         location: ValueNormalizer.asTrimmedString(source.location),
         price: ValueNormalizer.asTrimmedString(source.price),
         open_time: ValueNormalizer.asNullableString(source.open_time),
         close_time: ValueNormalizer.asNullableString(source.close_time),
         infoLink: ValueNormalizer.asNullableString(source.info_link),
         removalReason: ValueNormalizer.asNullableString(source.removalReason),
      };
   }

   static normalizeTransportation(value) {
      const source = ItineraryItemFormatterHelper.asObject(value);
      const legs = Array.isArray(source.legs)
         ? source.legs.map((leg) => {
            const sourceLeg = ItineraryItemFormatterHelper.asObject(leg);

            return {
               ...sourceLeg,
               from_station: ValueNormalizer.asTrimmedString(sourceLeg.from_station),
               to_station: ValueNormalizer.asTrimmedString(sourceLeg.to_station),
               start_time: ValueNormalizer.asTrimmedString(sourceLeg.start_time),
               end_time: ValueNormalizer.asTrimmedString(sourceLeg.end_time),
            };
         })
         : [];
      const stations = Array.isArray(source.stations)
         ? source.stations.map((station) => {
            const sourceStation = ItineraryItemFormatterHelper.asObject(station);

            return {
               ...sourceStation,
               name: ValueNormalizer.asTrimmedString(sourceStation.name),
               transportation: ValueNormalizer.asTrimmedString(sourceStation.transportation),
               role: ValueNormalizer.asTrimmedString(sourceStation.role),
               type: ValueNormalizer.asTrimmedString(sourceStation.type),
               description: ValueNormalizer.asTrimmedString(sourceStation.description),
               x_coord: ValueNormalizer.normalizeNumber(sourceStation.x_coord),
               y_coord: ValueNormalizer.normalizeNumber(sourceStation.y_coord),
            };
         })
         : [];

      return {
         ...source,
         name: ValueNormalizer.asTrimmedString(source.name),
         main_station: ValueNormalizer.asNullableString(source.main_station),
         infoLink: ValueNormalizer.asNullableString(source.info_link),
         added_as_attraction: source.added_as_attraction === true,
         bulk_transit_evaluated: source.bulk_transit_evaluated === true,
         legs,
         stations,
         route: ValueNormalizer.asNullableString(source.route),
         route_marker_sequences: ValueNormalizer.asArray(source.route_marker_sequences).map(
            ValueNormalizer.asTrimmedStringList
         ),
         removalReason: ValueNormalizer.asNullableString(source.removalReason),
      };
   }

   static normalizeTalk(value) {
      const source = ItineraryItemFormatterHelper.asObject(value);

      return {
         ...source,
         name: ValueNormalizer.asTrimmedString(source.name),
         location: ValueNormalizer.asTrimmedString(source.location),
         start_time: ValueNormalizer.asTrimmedString(source.start_time),
         maximum_duration: ItineraryItemFormatterHelper.normalizeMaximumDuration(source.maximum_duration),
         end_time: ValueNormalizer.asTrimmedString(source.end_time),
         link: ValueNormalizer.asNullableString(source.link),
         removalReason: ValueNormalizer.asNullableString(source.removalReason),
         linked_animals: GuardiansTalkLinkedAnimalNormalizer.normalizeGuardiansTalkLinkedAnimals(
            source.linked_animals
         ),
      };
   }

   static normalizeGuardiansTalkForSave(value) {
      const source = ItineraryItemFormatterHelper.asObject(value);

      return {
         name: ValueNormalizer.asTrimmedString(source.name),
         start_time: ValueNormalizer.asNullableString(source.start_time),
         end_time: ValueNormalizer.asNullableString(source.end_time),
      };
   }

   static normalizeItineraryNamesForSave(items) {
      if (!Array.isArray(items)) {
         return [];
      }

      return items
         .map(ItineraryItemFormatterHelper.normalizeItineraryNameForSave)
         .filter(Boolean);
   }

   static normalizeWild(value) {
      const source = ItineraryItemFormatterHelper.asObject(value);

      return {
         ...source,
         name: ValueNormalizer.asTrimmedString(source.name),
         meeting_spot: ValueNormalizer.asTrimmedString(source.meeting_spot),
         region: ValueNormalizer.asTrimmedString(source.region),
         start_time: ValueNormalizer.asTrimmedString(source.start_time),
         maximum_duration: ItineraryItemFormatterHelper.normalizeMaximumDuration(source.maximum_duration),
         end_time: ValueNormalizer.asTrimmedString(source.end_time),
         link: ValueNormalizer.asNullableString(source.link),
         removalReason: ValueNormalizer.asNullableString(source.removalReason),
      };
   }

   static normalizeWildEncounterForSave(value) {
      if (typeof value === 'string') {
         return WildEncounterScheduleItemKey.fromWire(value)?.toWire() ?? '';
      }

      return WildEncounterScheduleItemKey.fromRow(ItineraryItemFormatterHelper.asObject(value))?.toWire() ?? '';
   }

   static normalizeWildEncounterListForSave(items) {
      if (!Array.isArray(items)) {
         return [];
      }

      return items
         .map(ItineraryItemFormatter.normalizeWildEncounterForSave)
         .filter(Boolean);
   }
}
