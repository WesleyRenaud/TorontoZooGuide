import { StoredSelection } from '../base/storedSelection.js';
import { GuardiansTalkScheduleItemKey } from './guardiansTalkScheduleItemKey.js';
import { ScheduledOccurrencePresentation } from '../../scheduledOccurrencePresentation.js';
import { ScheduledOccurrenceTimeRange } from '../../scheduledOccurrenceTimeRange.js';
import { Strings } from '../../../strings.js';

export class GuardiansTalkSelectorModel {
   static getGuardiansTalkName(row) {
      return typeof row?.name === 'string'
         ? row.name
         : '';
   }

   static getGuardiansTalkKey(row) {
      return GuardiansTalkScheduleItemKey.fromRow(row);
   }

   static formatGuardiansTalkTitleSuffix(name) {
      return ScheduledOccurrencePresentation.formatOccurrenceTitleSuffix(
         name,
         Strings.entityLabels.guardiansTalk
      );
   }

   static formatGuardiansTalkSearchTitle(name) {
      return ScheduledOccurrencePresentation.formatOccurrenceSearchTitle(
         name,
         Strings.entityLabels.guardiansTalk
      );
   }

   static getGuardiansTalkSearchTitle(row) {
      return GuardiansTalkSelectorModel.formatGuardiansTalkSearchTitle(
         GuardiansTalkSelectorModel.getGuardiansTalkName(row)
      );
   }

   static getGuardiansTalkTitleSuffix(row) {
      return GuardiansTalkSelectorModel.formatGuardiansTalkTitleSuffix(
         GuardiansTalkSelectorModel.getGuardiansTalkName(row)
      );
   }

   static getGuardiansTalkId(row) {
      return GuardiansTalkSelectorModel.getGuardiansTalkKey(row)?.toWire() ?? '';
   }

   static getGuardiansTalkLocation(row) {
      return typeof row?.location === 'string'
         ? row.location
         : '';
   }

   static getGuardiansTalkScheduleStart(row) {
      return StoredSelection.normalizeStoredString(row?.start_time);
   }

   static getGuardiansTalkSubtitle(row) {
      return ScheduledOccurrencePresentation.buildOccurrenceSubtitle({
         primaryValue: GuardiansTalkSelectorModel.getGuardiansTalkLocation(row),
         timeRange: ScheduledOccurrenceTimeRange.buildScheduledOccurrenceTimeRange(row),
      });
   }

   static buildGuardiansTalkImageSrc(row) {
      return ScheduledOccurrencePresentation.buildOccurrenceDetailImageSrc(
         'guardians-talks',
         GuardiansTalkSelectorModel.getGuardiansTalkName(row)
      );
   }

   static readGuardiansTalkStoredFields(item) {
      return {
         location: StoredSelection.normalizeStoredString(item?.location),
         start_time: StoredSelection.normalizeStoredString(item?.start_time),
         end_time: StoredSelection.normalizeStoredString(item?.end_time),
      };
   }

   static buildGuardiansTalkSelectionFields(row) {
      return {
         location: GuardiansTalkSelectorModel.getGuardiansTalkLocation(row),
         start_time: GuardiansTalkSelectorModel.getGuardiansTalkScheduleStart(row),
         end_time: StoredSelection.normalizeStoredString(row?.end_time),
      };
   }
}
