import { DetailImageSrc } from '../assets/detailImageSrc.js';
import { StoredSelection } from './selectors/base/storedSelection.js';

export class ScheduledOccurrencePresentation {
   static buildOccurrenceDetailImageSrc(imageDirectory, name) {
      if (!name) {
         return null;
      }

      return DetailImageSrc.buildDetailImageSrc(imageDirectory, name, {
         basePath: '../images/details',
      });
   }

   static formatOccurrenceTitleSuffix(name, label) {
      return StoredSelection.normalizeStoredString(name)
         ? ` ${label}`
         : '';
   }

   static formatOccurrenceSearchTitle(name, label) {
      const trimmed = StoredSelection.normalizeStoredString(name);

      return trimmed
         ? `${trimmed}${ScheduledOccurrencePresentation.formatOccurrenceTitleSuffix(trimmed, label)}`
         : label;
   }

   static buildOccurrenceSubtitle({
      primaryValue = '',
      timeRange = '',
   } = {}) {
      const parts = [primaryValue, timeRange].filter(Boolean);

      return parts.length > 0
         ? parts.join('  •  ')
         : '-';
   }
}
