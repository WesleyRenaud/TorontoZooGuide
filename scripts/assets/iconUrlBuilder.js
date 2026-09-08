import { ValueNormalizer } from '../api/valueNormalizer.js';
import { AssetKeyNormalizer } from './assetKeyNormalizer.js';

export class IconUrlBuilder {
   static buildCssUrl(path) {
      return `url("${path}")`;
   }

   static isOpenIconVariant(token) {
      const variantToken = ValueNormalizer.asTrimmedString(token).toLowerCase();
      return !variantToken || variantToken === 'open';
   }

   static buildAnimalIconPath(exhibit, species, variantToken) {
      const normalizedExhibit = AssetKeyNormalizer.normalize(exhibit);
      const normalizedAnimal = AssetKeyNormalizer.normalize(species);
      const normalizedVariant = ValueNormalizer.asTrimmedString(variantToken).toLowerCase();

      return `/images/icons/animals/${normalizedExhibit}/${normalizedAnimal}/${normalizedAnimal}-${normalizedVariant}.png`;
   }

   static buildAttractionIconPath(attractionName, variantToken) {
      const normalizedAttraction = AssetKeyNormalizer.normalize(attractionName);

      if (IconUrlBuilder.isOpenIconVariant(variantToken)) {
         return `/images/icons/attractions/${normalizedAttraction}-open.png`;
      }

      const normalizedVariant = ValueNormalizer.asTrimmedString(variantToken).toLowerCase();
      return `/images/icons/attractions/${normalizedAttraction}/${normalizedAttraction}-${normalizedVariant}.png`;
   }

   static buildGenericIconPath(iconName, variantToken) {
      const normalizedVariant = IconUrlBuilder.isOpenIconVariant(variantToken)
         ? 'open'
         : ValueNormalizer.asTrimmedString(variantToken).toLowerCase();

      return `/images/icons/${iconName}/${iconName}-${normalizedVariant}.png`;
   }
}
