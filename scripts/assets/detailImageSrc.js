import { normalizeAssetKey } from './normalizeAssetKey.js';

export function buildDetailImageSrc(imageDirectory, name, {
   basePath = 'images/details',
} = {}) {
   const file = normalizeAssetKey(String(name).trim());

   if (!file) {
      return null;
   }

   return `${basePath}/${imageDirectory}/${file}.png`;
}

export function buildDetailImageSrcFromParts(pathParts, {
   basePath = 'images/details',
} = {}) {
   const normalizedParts = pathParts
      .map((part) => normalizeAssetKey(part))
      .filter(Boolean);

   if (normalizedParts.length !== pathParts.length) {
      return null;
   }

   return `${basePath}/${normalizedParts.join('/')}.png`;
}
