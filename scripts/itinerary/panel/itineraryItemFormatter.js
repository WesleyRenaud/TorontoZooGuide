import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { NormalizeGuardiansTalkLinkedAnimals } from '../../guardians/normalizeGuardiansTalkLinkedAnimals.js';
import { WildEncounterScheduleItemKey } from '../selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';

function asObject(value) {
   return value && typeof value === 'object'
      ? value
      : {};
}

function normalizeOptionalText(value) {
   const text = ItineraryItemFormatter.normalizeText(value);
   return text || null;
}

function normalizeMaximumDuration(value) {
   const maximumDuration = ValueNormalizer.normalizeNumber(value);
   return maximumDuration && maximumDuration > 0 ? maximumDuration : null;
}

function normalizeItineraryNameForSave(value) {
   if (typeof value === 'string') {
      return ItineraryItemFormatter.normalizeText(value);
   }

   return ItineraryItemFormatter.normalizeText(asObject(value).name);
}

export class ItineraryItemFormatter {
   static normalizeNumber = ValueNormalizer.normalizeNumber;

   static normalizeText(value) {
      return ValueNormalizer.asTrimmedString(value);
   }

   static normalizeNonNegativeNumber(value) {
      const number = ValueNormalizer.normalizeNumber(value);

      if (number == null || number < 0) {
         return null;
      }

      return number;
   }

   static parseDurationMinutes(value) {
      const normalized = String(value ?? '').trim();

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
      const source = asObject(value);

      return {
         ...source,
         species: ItineraryItemFormatter.normalizeText(source.species),
         exhibit: ItineraryItemFormatter.normalizeText(source.exhibit),
         link: normalizeOptionalText(source.link),
         removalReason: normalizeOptionalText(source.removalReason),
         likelihoodBefore: ValueNormalizer.normalizeNumber(source.likelihoodBefore),
         likelihoodAfter: ValueNormalizer.normalizeNumber(source.likelihoodAfter),
      };
   }

   static normalizeAttraction(value) {
      const source = asObject(value);

      return {
         ...source,
         name: ItineraryItemFormatter.normalizeText(source.name),
         subtitle: ItineraryItemFormatter.normalizeText(source.subtitle),
         region: ItineraryItemFormatter.normalizeText(source.region),
         location: ItineraryItemFormatter.normalizeText(source.location),
         price: ItineraryItemFormatter.normalizeText(source.price),
         open_time: normalizeOptionalText(source.open_time),
         close_time: normalizeOptionalText(source.close_time),
         infoLink: normalizeOptionalText(source.info_link),
         removalReason: normalizeOptionalText(source.removalReason),
      };
   }

   static normalizeTransportation(value) {
      const source = asObject(value);
      const legs = Array.isArray(source.legs)
         ? source.legs.map((leg) => {
            const sourceLeg = asObject(leg);

            return {
               ...sourceLeg,
               from_station: ItineraryItemFormatter.normalizeText(sourceLeg.from_station),
               to_station: ItineraryItemFormatter.normalizeText(sourceLeg.to_station),
               start_time: ItineraryItemFormatter.normalizeText(sourceLeg.start_time),
               end_time: ItineraryItemFormatter.normalizeText(sourceLeg.end_time),
            };
         })
         : [];
      const stations = Array.isArray(source.stations)
         ? source.stations.map((station) => {
            const sourceStation = asObject(station);

            return {
               ...sourceStation,
               name: ItineraryItemFormatter.normalizeText(sourceStation.name),
               transportation: ItineraryItemFormatter.normalizeText(sourceStation.transportation),
               role: ItineraryItemFormatter.normalizeText(sourceStation.role),
               type: ItineraryItemFormatter.normalizeText(sourceStation.type),
               description: ItineraryItemFormatter.normalizeText(sourceStation.description),
               x_coord: ValueNormalizer.normalizeNumber(sourceStation.x_coord),
               y_coord: ValueNormalizer.normalizeNumber(sourceStation.y_coord),
            };
         })
         : [];

      return {
         ...source,
         name: ItineraryItemFormatter.normalizeText(source.name),
         main_station: normalizeOptionalText(source.main_station),
         infoLink: normalizeOptionalText(source.info_link),
         added_as_attraction: source.added_as_attraction === true,
         bulk_transit_evaluated: source.bulk_transit_evaluated === true,
         legs,
         stations,
         route: normalizeOptionalText(source.route),
         route_marker_sequences: ValueNormalizer.asArray(source.route_marker_sequences).map(
            ValueNormalizer.asTrimmedStringList
         ),
         removalReason: normalizeOptionalText(source.removalReason),
      };
   }

   static normalizeTalk(value) {
      const source = asObject(value);

      return {
         ...source,
         name: ItineraryItemFormatter.normalizeText(source.name),
         location: ItineraryItemFormatter.normalizeText(source.location),
         start_time: ItineraryItemFormatter.normalizeText(source.start_time),
         maximum_duration: normalizeMaximumDuration(source.maximum_duration),
         end_time: ItineraryItemFormatter.normalizeText(source.end_time),
         link: normalizeOptionalText(source.link),
         removalReason: normalizeOptionalText(source.removalReason),
         linked_animals: NormalizeGuardiansTalkLinkedAnimals.normalizeGuardiansTalkLinkedAnimals(
            source.linked_animals
         ),
      };
   }

   static normalizeGuardiansTalkForSave(value) {
      const source = asObject(value);

      return {
         name: ItineraryItemFormatter.normalizeText(source.name),
         start_time: normalizeOptionalText(source.start_time),
         end_time: normalizeOptionalText(source.end_time),
      };
   }

   static normalizeItineraryNamesForSave(items) {
      if (!Array.isArray(items)) {
         return [];
      }

      return items
         .map(normalizeItineraryNameForSave)
         .filter(Boolean);
   }

   static normalizeWild(value) {
      const source = asObject(value);

      return {
         ...source,
         name: ItineraryItemFormatter.normalizeText(source.name),
         meeting_spot: ItineraryItemFormatter.normalizeText(source.meeting_spot),
         region: ItineraryItemFormatter.normalizeText(source.region),
         start_time: ItineraryItemFormatter.normalizeText(source.start_time),
         maximum_duration: normalizeMaximumDuration(source.maximum_duration),
         end_time: ItineraryItemFormatter.normalizeText(source.end_time),
         link: normalizeOptionalText(source.link),
         removalReason: normalizeOptionalText(source.removalReason),
      };
   }

   static normalizeWildEncounterForSave(value) {
      if (typeof value === 'string') {
         return WildEncounterScheduleItemKey.fromWire(value)?.toWire() ?? '';
      }

      return WildEncounterScheduleItemKey.fromRow(asObject(value))?.toWire() ?? '';
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
