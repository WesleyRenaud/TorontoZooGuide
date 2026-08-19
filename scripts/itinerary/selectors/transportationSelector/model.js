import { normalizeStoredLink } from '../base/storedSelection.js';
import { buildOccurrenceDetailImageSrc } from '../../scheduledOccurrencePresentation.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../../strings.js';

function asObject(value) {
   return value && typeof value === 'object'
      ? value
      : {};
}

function normalizeStationName(value) {
   return typeof value === 'string'
      ? value.trim()
      : '';
}

export function getTransportationName(row) {
   return typeof row?.name === 'string'
      ? row.name.trim()
      : '';
}

export function getTransportationId(row) {
   return getTransportationName(row);
}

export function getTransportationInfoLink(row) {
   return normalizeStoredLink(row?.info_link);
}

export function buildTransportationImageSrc(row) {
   return buildOccurrenceDetailImageSrc('transportations', getTransportationName(row));
}

export function getTransportationLegs(row) {
   const legs = asObject(row).legs;

   return Array.isArray(legs)
      ? legs.map((leg) => asObject(leg))
      : [];
}

export function getTransportationFirstStation(row) {
   const legs = getTransportationLegs(row);

   if (legs.length > 0) {
      return normalizeStationName(legs[0].from_station);
   }

   return normalizeStationName(row?.main_station);
}

export function getTransportationLastStation(row) {
   const legs = getTransportationLegs(row);

   if (legs.length > 0) {
      return normalizeStationName(legs[legs.length - 1].to_station);
   }

   return normalizeStationName(row?.main_station);
}

export function buildTransportationStationsLine(row) {
   const firstStation = getTransportationFirstStation(row);
   const lastStation = getTransportationLastStation(row);

   if (!firstStation && !lastStation) {
      return '';
   }

   if (firstStation && lastStation && firstStation === lastStation) {
      return APP_STRINGS.labels.transportationRoundTrip(firstStation);
   }

   if (firstStation && lastStation) {
      return APP_STRINGS.labels.transportationStations(firstStation, lastStation);
   }

   return firstStation || lastStation;
}

export function isTransportationAddedAsAttraction(row) {
   return row?.added_as_attraction === true;
}

export function isScheduleItemTransportationRow(row) {
   if (!row || typeof row !== 'object') {
      return false;
   }

   if (row.scheduleItemKind === ScheduleItemKind.TRANSPORTATION.itemType) {
      return true;
   }

   return isTransportationAddedAsAttraction(row);
}
