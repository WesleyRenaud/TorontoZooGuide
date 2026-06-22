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
   primaryLabel,
   primaryValue = '',
   timeRange = '',
} = {}) {
   const primaryLine = primaryValue
      ? `${primaryLabel}: ${primaryValue}`
      : `${primaryLabel}: -`;

   return timeRange
      ? `${primaryLine}  •  Time: ${timeRange}`
      : primaryLine;
}
