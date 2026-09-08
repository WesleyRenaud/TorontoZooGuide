import { ValueNormalizer } from '../../api/valueNormalizer.js';

export class ScheduleItemEventLabels {
   static formatItineraryEventTypeLabel(eventType) {
      const normalized = ValueNormalizer.asTrimmedString(eventType);

      if (!normalized) {
         return '';
      }

      return normalized
         .split('_')
         .map((part) => (
            part
               ? `${part.charAt(0).toUpperCase()}${part.slice(1)}`
               : ''
         ))
         .join(' ');
   }
}
