import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';
import { ScheduledOccurrencePresenter } from '../../scheduledOccurrencePresenter.js';
import { ScheduledOccurrenceTimeModel } from '../../scheduledOccurrenceTimeModel.js';
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
      return ScheduledOccurrencePresenter.formatOccurrenceTitleSuffix(
         name,
         Strings.entityLabels.wildEncounter
      );
   }

   static formatWildEncounterSearchTitle(name) {
      return ScheduledOccurrencePresenter.formatOccurrenceSearchTitle(
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
      return StoredSelectionNormalizer.normalizeStoredLink(row?.link);
   }

   static getWildEncounterScheduleStart(row) {
      return StoredSelectionNormalizer.normalizeStoredString(row?.start_time);
   }

   static getWildEncounterSubtitle(row) {
      return ScheduledOccurrencePresenter.buildOccurrenceSubtitle({
         primaryValue: WildEncounterSelectorModel.getWildEncounterMeetingSpot(row),
         timeRange: ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange(row),
      });
   }

   static buildWildEncounterImageSrc(row) {
      return ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc(
         'wild-encounters',
         WildEncounterSelectorModel.getWildEncounterName(row)
      );
   }

   static readWildEncounterStoredFields(item) {
      return {
         meeting_spot: StoredSelectionNormalizer.normalizeStoredString(item?.meeting_spot),
         start_time: StoredSelectionNormalizer.normalizeStoredString(item?.start_time),
         end_time: StoredSelectionNormalizer.normalizeStoredString(item?.end_time),
      };
   }

   static buildWildEncounterSelectionFields(row) {
      return {
         meeting_spot: WildEncounterSelectorModel.getWildEncounterMeetingSpot(row),
         start_time: WildEncounterSelectorModel.getWildEncounterScheduleStart(row),
         end_time: StoredSelectionNormalizer.normalizeStoredString(row?.end_time),
      };
   }
}
