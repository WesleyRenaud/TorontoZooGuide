import { ValueNormalizer } from '../api/valueNormalizer.js';
import { AssetKeyNormalizer } from './assetKeyNormalizer.js';
import detailImages from '../../shared/detailImages.json' with { type: 'json' };

export class DetailImageBuilder {
   static BASE_PATH = detailImages.root;

   static buildDetailImageSrc(imageDirectory, name, {
      basePath = DetailImageBuilder.BASE_PATH,
   } = {}) {
      const file = AssetKeyNormalizer.normalize(ValueNormalizer.asTrimmedString(name));

      if (!file) {
         return null;
      }

      return `${basePath}/${imageDirectory}/${file}.png`;
   }

   static buildDetailImageSrcFromParts(pathParts, {
      basePath = DetailImageBuilder.BASE_PATH,
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
