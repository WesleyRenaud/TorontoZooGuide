import { DetailImageBuilder } from '../assets/detailImageBuilder.js';
import { StoredSelectionNormalizer } from './selectors/base/storedSelectionNormalizer.js';

export class ScheduledOccurrencePresenter {
   static buildOccurrenceDetailImageSrc(imageDirectory, name) {
      if (!name) {
         return null;
      }

      return DetailImageBuilder.buildDetailImageSrc(imageDirectory, name, {
         basePath: '../images/details',
      });
   }

   static formatOccurrenceTitleSuffix(name, label) {
      return StoredSelectionNormalizer.normalizeStoredString(name)
         ? ` ${label}`
         : '';
   }

   static formatOccurrenceSearchTitle(name, label) {
      const trimmed = StoredSelectionNormalizer.normalizeStoredString(name);

      return trimmed
         ? `${trimmed}${ScheduledOccurrencePresenter.formatOccurrenceTitleSuffix(trimmed, label)}`
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
