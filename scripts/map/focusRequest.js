import { ValueNormalizer } from '../api/valueNormalizer.js';

export class FocusRequest {
   static scheduleFocusRequest(focus, focusRequest) {
      if (!focusRequest?.row) {
         return;
      }

      const type = ValueNormalizer.asTrimmedString(String(focusRequest.type || ''));

      setTimeout(() => {
         focus.focus({
            row: focusRequest.row,
            type,
         });
      }, 0);
   }

   static normalizeSearchFocusRequest(payload) {
      if (!payload || typeof payload !== 'object') {
         return null;
      }

      const type = ValueNormalizer.asTrimmedString(String(payload.type || ''));

      if (!type) {
         return null;
      }

      return {
         type,
         row: {
            ...payload,
            type,
         },
      };
   }

   static resolveDeepLinkFocus(payload) {
      if (!payload) {
         return null;
      }

      if (payload && typeof payload === 'object' && payload.row) {
         const type = ValueNormalizer.asTrimmedString(String(payload.row.type || ''));

         if (!type) {
            return null;
         }

         return {
            mode: 'direct',
            focusRequest: {
               row: payload.row,
               type,
            },
         };
      }

      if (!payload.species) {
         return null;
      }

      return {
         mode: 'refetch',
         focusRequest: {
            type: 'animal',
            row: {
               type: 'animal',
               species: payload.species,
               exhibit: payload.exhibit ?? null,
            },
         },
      };
   }
}
