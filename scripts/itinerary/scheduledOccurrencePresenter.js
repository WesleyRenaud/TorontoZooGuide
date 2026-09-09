import { ValueNormalizer } from '../api/valueNormalizer.js';
import { DetailImageBuilder } from '../assets/detailImageBuilder.js';
import { Strings } from '../strings.js';

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
      return ValueNormalizer.asTrimmedString(name)
         ? ` ${label}`
         : '';
   }

   static formatOccurrenceSearchTitle(name, label) {
      const trimmed = ValueNormalizer.asTrimmedString(name);

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
         ? parts.join(Strings.format.subtitleSeparator)
         : Strings.format.emptySubtitle;
   }
}
