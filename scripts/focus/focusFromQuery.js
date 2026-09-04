import { ValueNormalizer } from '../api/valueNormalizer.js';

function getFocusRequestFromQuery(search = window.location.search) {
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

export class FocusFromQuery {
   static initFocusFromQuery({ onFocus } = {}) {
      const focusRequest = getFocusRequestFromQuery();

      if (!focusRequest || typeof onFocus !== 'function') {
         return;
      }

      onFocus(focusRequest);

      history.replaceState({}, '', window.location.pathname);
   }
}
