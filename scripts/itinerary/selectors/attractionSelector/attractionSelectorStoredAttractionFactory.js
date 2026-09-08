import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';

export class AttractionSelectorStoredAttractionFactory {
   static createStoredAttractionFromString(item) {
      const name = ValueNormalizer.asTrimmedString(item);

      if (!name) {
         return null;
      }

      return {
         id: name,
         name,
         subtitle: '',
         freeWithAdmission: false,
         seasonal: false,
         isClosed: false,
         addedAsAttraction: false,
         infoLink: null,
         imageSrc: null,
      };
   }

   static createStoredAttractionFromObject(item) {
      const name = ValueNormalizer.asTrimmedString(item.name);
      const id = StoredSelectionNormalizer.normalizeStoredId(item.id, name);

      if (!id) {
         return null;
      }

      return {
         id,
         name,
         subtitle: ValueNormalizer.asTrimmedString(item.subtitle),
         freeWithAdmission: StoredSelectionNormalizer.normalizeStoredBoolean(item.freeWithAdmission),
         seasonal: StoredSelectionNormalizer.normalizeStoredBoolean(item.seasonal),
         isClosed: StoredSelectionNormalizer.normalizeStoredBoolean(item.isClosed),
         addedAsAttraction: StoredSelectionNormalizer.normalizeStoredBoolean(item.addedAsAttraction),
         infoLink: StoredSelectionNormalizer.normalizeStoredLink(item.infoLink),
         imageSrc: StoredSelectionNormalizer.normalizeStoredLink(item.imageSrc),
      };
   }
}
