import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { NormalizeGuardiansTalkLinkedAnimals } from '../../guardians/normalizeGuardiansTalkLinkedAnimals.js';
import { WildEncounterScheduleItemKey } from '../selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';

function asObject(value) {
   return value && typeof value === 'object'
      ? value
      : {};
}

function normalizeOptionalText(value) {
   const text = Format.normalizeText(value);
   return text || null;
}

function normalizeMaximumDuration(value) {
   const maximumDuration = ValueNormalizer.normalizeNumber(value);
   return maximumDuration && maximumDuration > 0 ? maximumDuration : null;
}

function normalizeItineraryNameForSave(value) {
   if (typeof value === 'string') {
      return Format.normalizeText(value);
   }

   return Format.normalizeText(asObject(value).name);
}

export class Format {
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
         species: Format.normalizeText(source.species),
         exhibit: Format.normalizeText(source.exhibit),
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
         name: Format.normalizeText(source.name),
         subtitle: Format.normalizeText(source.subtitle),
         region: Format.normalizeText(source.region),
         location: Format.normalizeText(source.location),
         price: Format.normalizeText(source.price),
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
               from_station: Format.normalizeText(sourceLeg.from_station),
               to_station: Format.normalizeText(sourceLeg.to_station),
               start_time: Format.normalizeText(sourceLeg.start_time),
               end_time: Format.normalizeText(sourceLeg.end_time),
            };
         })
         : [];
      const stations = Array.isArray(source.stations)
         ? source.stations.map((station) => {
            const sourceStation = asObject(station);

            return {
               ...sourceStation,
               name: Format.normalizeText(sourceStation.name),
               transportation: Format.normalizeText(sourceStation.transportation),
               role: Format.normalizeText(sourceStation.role),
               type: Format.normalizeText(sourceStation.type),
               description: Format.normalizeText(sourceStation.description),
               x_coord: ValueNormalizer.normalizeNumber(sourceStation.x_coord),
               y_coord: ValueNormalizer.normalizeNumber(sourceStation.y_coord),
            };
         })
         : [];

      return {
         ...source,
         name: Format.normalizeText(source.name),
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
         name: Format.normalizeText(source.name),
         location: Format.normalizeText(source.location),
         start_time: Format.normalizeText(source.start_time),
         maximum_duration: normalizeMaximumDuration(source.maximum_duration),
         end_time: Format.normalizeText(source.end_time),
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
         name: Format.normalizeText(source.name),
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
         name: Format.normalizeText(source.name),
         meeting_spot: Format.normalizeText(source.meeting_spot),
         region: Format.normalizeText(source.region),
         start_time: Format.normalizeText(source.start_time),
         maximum_duration: normalizeMaximumDuration(source.maximum_duration),
         end_time: Format.normalizeText(source.end_time),
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
         .map(Format.normalizeWildEncounterForSave)
         .filter(Boolean);
   }
}
