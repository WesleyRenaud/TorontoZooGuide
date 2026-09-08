import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ItineraryItemFormatter } from '../panel/itineraryItemFormatter.js';

export class WarningFixedTimeDraftFilter {
   static fixedTimeOccurrenceKey(row = {}) {
      const name = ValueNormalizer.asTrimmedString(row.name).toLowerCase();
      const startTime = ItineraryItemFormatter.formatClockTime(row.start_time);

      if (!name) {
         return '';
      }

      return startTime
         ? `${name}\0${startTime}`
         : `name:${name}`;
   }

   static rejectedOccurrenceKeys(items, isItemType) {
      return new Set(
         items
            .filter(isItemType)
            .map(WarningFixedTimeDraftFilter.fixedTimeOccurrenceKey)
            .filter(Boolean)
      );
   }

   static keepDraftItem(row, rejectedKeys) {
      const key = WarningFixedTimeDraftFilter.fixedTimeOccurrenceKey(row);

      if (key && rejectedKeys.has(key)) {
         return false;
      }

      const nameKey = `name:${ValueNormalizer.asTrimmedString(row.name).toLowerCase()}`;

      return !rejectedKeys.has(nameKey);
   }
}
