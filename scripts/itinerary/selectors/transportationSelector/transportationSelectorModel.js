import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { StoredSelection } from '../base/storedSelection.js';
import { ScheduledOccurrencePresentation } from '../../scheduledOccurrencePresentation.js';
import { ScheduledOccurrenceTimeRange } from '../../scheduledOccurrenceTimeRange.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../../strings.js';
import { TransportationScheduleItemKey } from './transportationScheduleItemKey.js';
import { TransportationStationNameResolver } from './transportationStationNameResolver.js';

export class TransportationSelectorModel {
   static getTransportationName(row) {
      return ValueNormalizer.asTrimmedString(row?.name);
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
      const stations = TransportationStationNameResolver.asObject(row).stations;

      return Array.isArray(stations)
         ? stations.map((station) => TransportationStationNameResolver.asObject(station))
         : [];
   }

   static isTransportationScheduled(row) {
      return TransportationStationNameResolver.getTransportationLegs(row).length > 0;
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
      const [firstStation] = TransportationStationNameResolver.boardingStationNames(row);
      const offboarding = TransportationStationNameResolver.offboardingStationNames(row);
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
         fromString: TransportationStationNameResolver.createStoredTransportationFromString,
         fromObject: TransportationStationNameResolver.createStoredTransportationFromObject,
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
