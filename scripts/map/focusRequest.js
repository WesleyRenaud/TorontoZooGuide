export function scheduleFocusRequest(focus, focusRequest) {
   if (!focusRequest?.row) {
      return;
   }

   const type = String(focusRequest.type || '').trim();

   setTimeout(() => {
      focus.focus({
         row: focusRequest.row,
         type,
      });
   }, 0);
}

export function normalizeSearchFocusRequest(payload) {
   if (!payload || typeof payload !== 'object') {
      return null;
   }

   const type = String(payload.type || '').trim();

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

export function resolveDeepLinkFocus(payload) {
   if (!payload) {
      return null;
   }

   if (payload && typeof payload === 'object' && payload.row) {
      const type = String(payload.row.type || '').trim();

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
