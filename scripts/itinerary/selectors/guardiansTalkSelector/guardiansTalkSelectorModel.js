import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';
import { GuardiansTalkScheduleItemKey } from './guardiansTalkScheduleItemKey.js';
import { ScheduledOccurrencePresenter } from '../../scheduledOccurrencePresenter.js';
import { ScheduledOccurrenceTimeModel } from '../../scheduledOccurrenceTimeModel.js';
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
      return ScheduledOccurrencePresenter.formatOccurrenceTitleSuffix(
         name,
         Strings.entityLabels.guardiansTalk
      );
   }

   static formatGuardiansTalkSearchTitle(name) {
      return ScheduledOccurrencePresenter.formatOccurrenceSearchTitle(
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
      return StoredSelectionNormalizer.normalizeStoredString(row?.start_time);
   }

   static getGuardiansTalkSubtitle(row) {
      return ScheduledOccurrencePresenter.buildOccurrenceSubtitle({
         primaryValue: GuardiansTalkSelectorModel.getGuardiansTalkLocation(row),
         timeRange: ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange(row),
      });
   }

   static buildGuardiansTalkImageSrc(row) {
      return ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc(
         'guardians-talks',
         GuardiansTalkSelectorModel.getGuardiansTalkName(row)
      );
   }

   static readGuardiansTalkStoredFields(item) {
      return {
         location: StoredSelectionNormalizer.normalizeStoredString(item?.location),
         start_time: StoredSelectionNormalizer.normalizeStoredString(item?.start_time),
         end_time: StoredSelectionNormalizer.normalizeStoredString(item?.end_time),
      };
   }

   static buildGuardiansTalkSelectionFields(row) {
      return {
         location: GuardiansTalkSelectorModel.getGuardiansTalkLocation(row),
         start_time: GuardiansTalkSelectorModel.getGuardiansTalkScheduleStart(row),
         end_time: StoredSelectionNormalizer.normalizeStoredString(row?.end_time),
      };
   }
}
