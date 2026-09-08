import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { StoredSelection } from '../base/storedSelection.js';

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
      const id = StoredSelection.normalizeStoredId(item.id, name);

      if (!id) {
         return null;
      }

      return {
         id,
         name,
         subtitle: ValueNormalizer.asTrimmedString(item.subtitle),
         freeWithAdmission: StoredSelection.normalizeStoredBoolean(item.freeWithAdmission),
         seasonal: StoredSelection.normalizeStoredBoolean(item.seasonal),
         isClosed: StoredSelection.normalizeStoredBoolean(item.isClosed),
         addedAsAttraction: StoredSelection.normalizeStoredBoolean(item.addedAsAttraction),
         infoLink: StoredSelection.normalizeStoredLink(item.infoLink),
         imageSrc: StoredSelection.normalizeStoredLink(item.imageSrc),
      };
   }
}
