import {
   migrateStoredSelectionItems,
   normalizeStoredBoolean,
   normalizeStoredId,
   normalizeStoredLink,
   normalizeStoredString,
} from '../base/storedSelection.js';
import {
   getItineraryTransportationStationOffboardingRoles,
   getItineraryTransportationStationOnboardingRoles,
} from '../../itineraryTransportationStationRoles.js';
import {
   buildOccurrenceDetailImageSrc,
   buildOccurrenceSubtitle,
} from '../../scheduledOccurrencePresentation.js';
import { buildScheduledOccurrenceTimeRange } from '../../scheduledOccurrenceTimeRange.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../../strings.js';

function asObject(value) {
   return value && typeof value === 'object'
      ? value
      : {};
}

function uniqueNames(names) {
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

function namesForRoles(stations, roles) {
   return uniqueNames(
      stations
         .filter((station) => roles.includes(station.role))
         .map((station) => normalizeStoredString(station.name))
   );
}

function getTransportationLegs(row) {
   const legs = asObject(row).legs;

   return Array.isArray(legs)
      ? legs.map((leg) => asObject(leg))
      : [];
}

function fallbackStationNames(row, pickFromLeg) {
   const legs = getTransportationLegs(row);

   if (legs.length > 0) {
      const name = normalizeStoredString(pickFromLeg(legs));
      return name ? [name] : [];
   }

   if (!isTransportationAddedAsAttraction(row)) {
      return [];
   }

   const mainStation = normalizeStoredString(row?.main_station);
   return mainStation ? [mainStation] : [];
}

function boardingStationNames(row) {
   const stations = getTransportationStations(row);

   if (stations.length > 0) {
      return namesForRoles(
         stations,
         getItineraryTransportationStationOnboardingRoles()
      );
   }

   return fallbackStationNames(row, (legs) => legs[0].from_station);
}

function offboardingStationNames(row) {
   const stations = getTransportationStations(row);

   if (stations.length > 0) {
      return namesForRoles(
         stations,
         getItineraryTransportationStationOffboardingRoles()
      );
   }

   return fallbackStationNames(row, (legs) => legs[legs.length - 1].to_station);
}

export function getTransportationName(row) {
   return normalizeStoredString(row?.name);
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

export function getTransportationStations(row) {
   const stations = asObject(row).stations;

   return Array.isArray(stations)
      ? stations.map((station) => asObject(station))
      : [];
}

export function isTransportationScheduled(row) {
   return getTransportationLegs(row).length > 0;
}

export function buildTransportationStationsLine(row) {
   const [firstStation] = boardingStationNames(row);
   const offboarding = offboardingStationNames(row);
   const lastStation = offboarding[offboarding.length - 1];

   if (!firstStation && !lastStation) {
      return '';
   }

   if (firstStation && lastStation && firstStation !== lastStation) {
      return APP_STRINGS.labels.transportationStations(firstStation, lastStation);
   }

   if (firstStation && lastStation) {
      return APP_STRINGS.labels.transportationRoundTrip(firstStation);
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

export function getTransportationTitle(row) {
   return getTransportationName(row) || APP_STRINGS.entityLabels.transportation;
}

export function isAlsoAttractionTransportation(row) {
   return row?.is_also_attraction === true;
}

export function shouldConfirmAddAsTransportation({
   row,
   isSelected,
} = {}) {
   if (isSelected) {
      return false;
   }

   return isAlsoAttractionTransportation(row);
}

export function buildAddAsTransportationMessage(row) {
   return APP_STRINGS.itinerary.confirmation.addAsTransportationMessage(
      getTransportationName(row)
   );
}

export function isFreeWithAdmissionTransportation(row) {
   return row?.free_with_admission === true;
}

export function getTransportationSubtitle(row) {
   return buildOccurrenceSubtitle({
      primaryValue: isFreeWithAdmissionTransportation(row)
         ? APP_STRINGS.search.freeWithAdmission
         : APP_STRINGS.search.extraCharge,
      timeRange: buildScheduledOccurrenceTimeRange({
         start_time: row?.open_time,
         end_time: row?.close_time,
      }),
   });
}

function createStoredTransportationFromString(item) {
   const name = normalizeStoredString(item);

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

function createStoredTransportationFromObject(item) {
   const name = normalizeStoredString(item.name);
   const id = normalizeStoredId(item.id, name);

   if (!id) {
      return null;
   }

   return {
      id,
      name,
      subtitle: normalizeStoredString(item.subtitle),
      infoLink: normalizeStoredLink(item.infoLink),
      imageSrc: normalizeStoredLink(item.imageSrc),
      addedAsAttraction: normalizeStoredBoolean(item.addedAsAttraction),
   };
}

export function migrateStoredTransportations(items) {
   return migrateStoredSelectionItems(items, {
      fromString: createStoredTransportationFromString,
      fromObject: createStoredTransportationFromObject,
   });
}

export function makeTransportationSelection(row) {
   return {
      id: getTransportationId(row),
      name: getTransportationName(row),
      subtitle: buildTransportationStationsLine(row) || getTransportationSubtitle(row),
      infoLink: getTransportationInfoLink(row),
      imageSrc: buildTransportationImageSrc(row),
      addedAsAttraction: false,
   };
}
