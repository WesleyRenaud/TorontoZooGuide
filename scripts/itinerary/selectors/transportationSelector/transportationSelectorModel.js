import { StoredSelection } from '../base/storedSelection.js';
import { ItineraryTransportationStationRoles } from '../../itineraryTransportationStationRoles.js';
import { ScheduledOccurrencePresentation } from '../../scheduledOccurrencePresentation.js';
import { ScheduledOccurrenceTimeRange } from '../../scheduledOccurrenceTimeRange.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../../strings.js';
import { TransportationScheduleItemKey } from './transportationScheduleItemKey.js';

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
         .map((station) => StoredSelection.normalizeStoredString(station.name))
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
      const name = StoredSelection.normalizeStoredString(pickFromLeg(legs));
      return name ? [name] : [];
   }

   if (!TransportationSelectorModel.isTransportationAddedAsAttraction(row)) {
      return [];
   }

   const mainStation = StoredSelection.normalizeStoredString(row?.main_station);
   return mainStation ? [mainStation] : [];
}

function boardingStationNames(row) {
   const stations = TransportationSelectorModel.getTransportationStations(row);

   if (stations.length > 0) {
      return namesForRoles(
         stations,
         ItineraryTransportationStationRoles.getItineraryTransportationStationOnboardingRoles()
      );
   }

   return fallbackStationNames(row, (legs) => legs[0].from_station);
}

function offboardingStationNames(row) {
   const stations = TransportationSelectorModel.getTransportationStations(row);

   if (stations.length > 0) {
      return namesForRoles(
         stations,
         ItineraryTransportationStationRoles.getItineraryTransportationStationOffboardingRoles()
      );
   }

   return fallbackStationNames(row, (legs) => legs[legs.length - 1].to_station);
}

function createStoredTransportationFromString(item) {
   const name = StoredSelection.normalizeStoredString(item);

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
   const name = StoredSelection.normalizeStoredString(item.name);
   const id = StoredSelection.normalizeStoredId(item.id, name);

   if (!id) {
      return null;
   }

   return {
      id,
      name,
      subtitle: StoredSelection.normalizeStoredString(item.subtitle),
      infoLink: StoredSelection.normalizeStoredLink(item.infoLink),
      imageSrc: StoredSelection.normalizeStoredLink(item.imageSrc),
      addedAsAttraction: StoredSelection.normalizeStoredBoolean(item.addedAsAttraction),
   };
}

export class TransportationSelectorModel {
   static getTransportationName(row) {
      return StoredSelection.normalizeStoredString(row?.name);
   }

   static getTransportationId(row) {
      return TransportationSelectorModel.getTransportationName(row);
   }

   static getTransportationScheduleItemKey(row) {
      return TransportationScheduleItemKey.fromRow(row)?.toWire() ?? '';
   }

   static getTransportationInfoLink(row) {
      return StoredSelection.normalizeStoredLink(row?.info_link);
   }

   static buildTransportationImageSrc(row) {
      return ScheduledOccurrencePresentation.buildOccurrenceDetailImageSrc(
         'transportations',
         TransportationSelectorModel.getTransportationName(row)
      );
   }

   static getTransportationStations(row) {
      const stations = asObject(row).stations;

      return Array.isArray(stations)
         ? stations.map((station) => asObject(station))
         : [];
   }

   static isTransportationScheduled(row) {
      return getTransportationLegs(row).length > 0;
   }

   static isBulkTransitEvaluated(row) {
      return row?.bulk_transit_evaluated === true;
   }

   static isTransitTransportationHandledForDayPlanner(row) {
      if (TransportationSelectorModel.isTransportationAddedAsAttraction(row)) {
         return Boolean(row?.start_time && row?.end_time);
      }

      return TransportationSelectorModel.isBulkTransitEvaluated(row);
   }

   static buildTransportationStationsLine(row) {
      const [firstStation] = boardingStationNames(row);
      const offboarding = offboardingStationNames(row);
      const lastStation = offboarding[offboarding.length - 1];

      if (!firstStation && !lastStation) {
         return '';
      }

      if (firstStation && lastStation && firstStation !== lastStation) {
         return Strings.labels.transportationStations(firstStation, lastStation);
      }

      if (firstStation && lastStation) {
         return Strings.labels.transportationRoundTrip(firstStation);
      }

      return firstStation || lastStation;
   }

   static isTransportationAddedAsAttraction(row) {
      return row?.added_as_attraction === true;
   }

   static isScheduleItemTransportationRow(row) {
      if (!row || typeof row !== 'object') {
         return false;
      }

      if (row.scheduleItemKind === ScheduleItemKind.TRANSPORTATION.itemType) {
         return true;
      }

      return TransportationSelectorModel.isTransportationAddedAsAttraction(row);
   }

   static getTransportationTitle(row) {
      return TransportationSelectorModel.getTransportationName(row)
         || Strings.entityLabels.transportation;
   }

   static isAlsoAttractionTransportation(row) {
      return row?.is_also_attraction === true;
   }

   static shouldConfirmAddAsTransportation({
      row,
      isSelected,
   } = {}) {
      if (isSelected) {
         return false;
      }

      return TransportationSelectorModel.isAlsoAttractionTransportation(row);
   }

   static buildAddAsTransportationMessage(row) {
      return Strings.itinerary.confirmation.addAsTransportationMessage(
         TransportationSelectorModel.getTransportationName(row)
      );
   }

   static isFreeWithAdmissionTransportation(row) {
      return row?.free_with_admission === true;
   }

   static getTransportationSubtitle(row) {
      return ScheduledOccurrencePresentation.buildOccurrenceSubtitle({
         primaryValue: TransportationSelectorModel.isFreeWithAdmissionTransportation(row)
            ? Strings.search.freeWithAdmission
            : Strings.search.extraCharge,
         timeRange: ScheduledOccurrenceTimeRange.buildScheduledOccurrenceTimeRange({
            start_time: row?.open_time,
            end_time: row?.close_time,
         }),
      });
   }

   static migrateStoredTransportations(items) {
      return StoredSelection.migrateStoredSelectionItems(items, {
         fromString: createStoredTransportationFromString,
         fromObject: createStoredTransportationFromObject,
      });
   }

   static makeTransportationSelection(row) {
      return {
         id: TransportationSelectorModel.getTransportationId(row),
         name: TransportationSelectorModel.getTransportationName(row),
         subtitle: TransportationSelectorModel.buildTransportationStationsLine(row)
            || TransportationSelectorModel.getTransportationSubtitle(row),
         infoLink: TransportationSelectorModel.getTransportationInfoLink(row),
         imageSrc: TransportationSelectorModel.buildTransportationImageSrc(row),
         addedAsAttraction: false,
      };
   }
}
