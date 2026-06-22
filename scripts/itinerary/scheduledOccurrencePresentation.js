import { buildDetailImageSrc } from '../assets/detailImageSrc.js';

export function buildOccurrenceDetailImageSrc(imageDirectory, name) {
   if (!name) {
      return null;
   }

   return buildDetailImageSrc(imageDirectory, name, {
      basePath: '../images/details',
   });
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
