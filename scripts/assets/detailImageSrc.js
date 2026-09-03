import { AssetKeyNormalizer } from './assetKeyNormalizer.js';

export class DetailImageSrc {
   static buildDetailImageSrc(imageDirectory, name, {
      basePath = 'images/details',
   } = {}) {
      const file = AssetKeyNormalizer.normalize(String(name).trim());

      if (!file) {
         return null;
      }

      return `${basePath}/${imageDirectory}/${file}.png`;
   }

   static buildDetailImageSrcFromParts(pathParts, {
      basePath = 'images/details',
   } = {}) {
      const normalizedParts = pathParts
         .map((part) => AssetKeyNormalizer.normalize(part))
         .filter(Boolean);

      if (normalizedParts.length !== pathParts.length) {
         return null;
      }

      return `${basePath}/${normalizedParts.join('/')}.png`;
   }
}
