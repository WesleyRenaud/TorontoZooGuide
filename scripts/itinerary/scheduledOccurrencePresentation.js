import { ValueNormalizer } from '../api/valueNormalizer.js';
import { DetailImageSrc } from '../assets/detailImageSrc.js';

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
      return ValueNormalizer.asTrimmedString(name)
         ? ` ${label}`
         : '';
   }

   static formatOccurrenceSearchTitle(name, label) {
      const trimmed = ValueNormalizer.asTrimmedString(name);

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
