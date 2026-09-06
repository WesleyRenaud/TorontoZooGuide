import { StoredSelection } from '../base/storedSelection.js';
import { ScheduledOccurrencePresentation } from '../../scheduledOccurrencePresentation.js';
import { ScheduledOccurrenceTimeRange } from '../../scheduledOccurrenceTimeRange.js';
import { Strings } from '../../../strings.js';
import { WildEncounterScheduleItemKey } from './wildEncounterScheduleItemKey.js';

export class WildEncounterSelectorModel {
   static getWildEncounterName(row) {
      return typeof row?.name === 'string'
         ? row.name
         : '';
   }

   static getWildEncounterKey(row) {
      return WildEncounterScheduleItemKey.fromRow(row);
   }

   static getWildEncounterId(row) {
      return WildEncounterSelectorModel.getWildEncounterKey(row).toWire();
   }

   static formatWildEncounterTitleSuffix(name) {
      return ScheduledOccurrencePresentation.formatOccurrenceTitleSuffix(
         name,
         Strings.entityLabels.wildEncounter
      );
   }

   static formatWildEncounterSearchTitle(name) {
      return ScheduledOccurrencePresentation.formatOccurrenceSearchTitle(
         name,
         Strings.entityLabels.wildEncounter
      );
   }

   static getWildEncounterSearchTitle(row) {
      return WildEncounterSelectorModel.formatWildEncounterSearchTitle(
         WildEncounterSelectorModel.getWildEncounterName(row)
      );
   }

   static getWildEncounterTitleSuffix(row) {
      return WildEncounterSelectorModel.formatWildEncounterTitleSuffix(
         WildEncounterSelectorModel.getWildEncounterName(row)
      );
   }

   static getWildEncounterMeetingSpot(row) {
      return typeof row?.meeting_spot === 'string'
         ? row.meeting_spot
         : '';
   }

   static getWildEncounterLink(row) {
      return StoredSelection.normalizeStoredLink(row?.link);
   }

   static getWildEncounterScheduleStart(row) {
      return StoredSelection.normalizeStoredString(row?.start_time);
   }

   static getWildEncounterSubtitle(row) {
      return ScheduledOccurrencePresentation.buildOccurrenceSubtitle({
         primaryValue: WildEncounterSelectorModel.getWildEncounterMeetingSpot(row),
         timeRange: ScheduledOccurrenceTimeRange.buildScheduledOccurrenceTimeRange(row),
      });
   }

   static buildWildEncounterImageSrc(row) {
      return ScheduledOccurrencePresentation.buildOccurrenceDetailImageSrc(
         'wild-encounters',
         WildEncounterSelectorModel.getWildEncounterName(row)
      );
   }

   static readWildEncounterStoredFields(item) {
      return {
         meeting_spot: StoredSelection.normalizeStoredString(item?.meeting_spot),
         start_time: StoredSelection.normalizeStoredString(item?.start_time),
         end_time: StoredSelection.normalizeStoredString(item?.end_time),
      };
   }

   static buildWildEncounterSelectionFields(row) {
      return {
         meeting_spot: WildEncounterSelectorModel.getWildEncounterMeetingSpot(row),
         start_time: WildEncounterSelectorModel.getWildEncounterScheduleStart(row),
         end_time: StoredSelection.normalizeStoredString(row?.end_time),
      };
   }
}
