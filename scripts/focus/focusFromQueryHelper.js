import { ValueNormalizer } from '../api/valueNormalizer.js';

export class FocusFromQueryHelper {
   static getFocusRequestFromQuery(search = window.location.search) {
      const params = new URLSearchParams(search);
      const species = ValueNormalizer.asTrimmedString(params.get('focus'));

      if (!species) {
         return null;
      }

      const exhibit = ValueNormalizer.asNullableString(params.get('exhibit'));

      return {
         species,
         exhibit,
      };
   }
}
