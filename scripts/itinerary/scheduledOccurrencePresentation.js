import { buildDetailImageSrc } from '../assets/detailImageSrc.js';
import { normalizeStoredString } from './selectors/base/storedSelection.js';

export function buildOccurrenceDetailImageSrc(imageDirectory, name) {
   if (!name) {
      return null;
   }

   return buildDetailImageSrc(imageDirectory, name, {
      basePath: '../images/details',
   });
}

export function formatOccurrenceTitleSuffix(name, label) {
   return normalizeStoredString(name)
      ? ` ${label}`
      : '';
}

export function formatOccurrenceSearchTitle(name, label) {
   const trimmed = normalizeStoredString(name);

   return trimmed
      ? `${trimmed}${formatOccurrenceTitleSuffix(trimmed, label)}`
      : label;
}

export function buildOccurrenceSubtitle({
   primaryValue = '',
   timeRange = '',
} = {}) {
   const parts = [primaryValue, timeRange].filter(Boolean);

   return parts.length > 0
      ? parts.join('  •  ')
      : '-';
}
