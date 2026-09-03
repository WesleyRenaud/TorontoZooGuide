import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { normalizeGuardiansTalkLinkedAnimals } from '../../guardians/normalizeGuardiansTalkLinkedAnimals.js';
import { WildEncounterScheduleItemKey } from '../selectors/wildEncounterSelector/scheduleItemKey.js';

export const normalizeNumber = ValueNormalizer.normalizeNumber;

function asObject(value) {
   return value && typeof value === 'object'
      ? value
      : {};
}

export function normalizeText(value) {
   return typeof value === 'string'
      ? value.trim()
      : '';
}

function normalizeOptionalText(value) {
   const text = normalizeText(value);
   return text || null;
}

export function normalizeNonNegativeNumber(value) {
   const number = ValueNormalizer.normalizeNumber(value);

   if (number == null || number < 0) {
      return null;
   }

   return number;
}

export function parseDurationMinutes(value) {
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

function normalizeMaximumDuration(value) {
   const maximumDuration = ValueNormalizer.normalizeNumber(value);
   return maximumDuration && maximumDuration > 0 ? maximumDuration : null;
}

export function formatISODateLong(iso) {
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

export function formatISODateFull(iso, fallback = '') {
   if (!iso || typeof iso !== 'string') return fallback;

   const dateParts = iso.trim().match(/^(\d{4})-(\d{2})-(\d{2})$/);

   if (!dateParts) {
      return iso.trim() || fallback;
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

export function formatClockTime(timeValue, fallback = '') {
   if (typeof timeValue !== 'string' || !timeValue.trim()) {
      return fallback;
   }

   const timeParts = timeValue.trim().match(/^(\d{1,2}):(\d{2})(?::(\d{2}))?$/);

   if (!timeParts) {
      return timeValue.trim();
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

export function normalizeAnimal(value) {
   const source = asObject(value);

   return {
      ...source,
      species: normalizeText(source.species),
      exhibit: normalizeText(source.exhibit),
      link: normalizeOptionalText(source.link),
      removalReason: normalizeOptionalText(source.removalReason),
      likelihoodBefore: ValueNormalizer.normalizeNumber(source.likelihoodBefore),
      likelihoodAfter: ValueNormalizer.normalizeNumber(source.likelihoodAfter),
   };
}

export function normalizeAttraction(value) {
   const source = asObject(value);

   return {
      ...source,
      name: normalizeText(source.name),
      subtitle: normalizeText(source.subtitle),
      region: normalizeText(source.region),
      location: normalizeText(source.location),
      price: normalizeText(source.price),
      open_time: normalizeOptionalText(source.open_time),
      close_time: normalizeOptionalText(source.close_time),
      infoLink: normalizeOptionalText(source.info_link),
      removalReason: normalizeOptionalText(source.removalReason),
   };
}

export function normalizeTransportation(value) {
   const source = asObject(value);
   const legs = Array.isArray(source.legs)
      ? source.legs.map((leg) => {
         const sourceLeg = asObject(leg);

         return {
            ...sourceLeg,
            from_station: normalizeText(sourceLeg.from_station),
            to_station: normalizeText(sourceLeg.to_station),
            start_time: normalizeText(sourceLeg.start_time),
            end_time: normalizeText(sourceLeg.end_time),
         };
      })
      : [];
   const stations = Array.isArray(source.stations)
      ? source.stations.map((station) => {
         const sourceStation = asObject(station);

         return {
            ...sourceStation,
            name: normalizeText(sourceStation.name),
            transportation: normalizeText(sourceStation.transportation),
            role: normalizeText(sourceStation.role),
            type: normalizeText(sourceStation.type),
            description: normalizeText(sourceStation.description),
            x_coord: ValueNormalizer.normalizeNumber(sourceStation.x_coord),
            y_coord: ValueNormalizer.normalizeNumber(sourceStation.y_coord),
         };
      })
      : [];

   return {
      ...source,
      name: normalizeText(source.name),
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

export function normalizeTalk(value) {
   const source = asObject(value);

   return {
      ...source,
      name: normalizeText(source.name),
      location: normalizeText(source.location),
      start_time: normalizeText(source.start_time),
      maximum_duration: normalizeMaximumDuration(source.maximum_duration),
      end_time: normalizeText(source.end_time),
      link: normalizeOptionalText(source.link),
      removalReason: normalizeOptionalText(source.removalReason),
      linked_animals: normalizeGuardiansTalkLinkedAnimals(source.linked_animals),
   };
}

export function normalizeGuardiansTalkForSave(value) {
   const source = asObject(value);

   return {
      name: normalizeText(source.name),
      start_time: normalizeOptionalText(source.start_time),
      end_time: normalizeOptionalText(source.end_time),
   };
}

function normalizeItineraryNameForSave(value) {
   if (typeof value === 'string') {
      return normalizeText(value);
   }

   return normalizeText(asObject(value).name);
}

export function normalizeItineraryNamesForSave(items) {
   if (!Array.isArray(items)) {
      return [];
   }

   return items
      .map(normalizeItineraryNameForSave)
      .filter(Boolean);
}

export function normalizeWild(value) {
   const source = asObject(value);

   return {
      ...source,
      name: normalizeText(source.name),
      meeting_spot: normalizeText(source.meeting_spot),
      region: normalizeText(source.region),
      start_time: normalizeText(source.start_time),
      maximum_duration: normalizeMaximumDuration(source.maximum_duration),
      end_time: normalizeText(source.end_time),
      link: normalizeOptionalText(source.link),
      removalReason: normalizeOptionalText(source.removalReason),
   };
}

export function normalizeWildEncounterForSave(value) {
   if (typeof value === 'string') {
      return WildEncounterScheduleItemKey.fromWire(value)?.toWire() ?? '';
   }

   return WildEncounterScheduleItemKey.fromRow(asObject(value))?.toWire() ?? '';
}

export function normalizeWildEncounterListForSave(items) {
   if (!Array.isArray(items)) {
      return [];
   }

   return items
      .map(normalizeWildEncounterForSave)
      .filter(Boolean);
}
