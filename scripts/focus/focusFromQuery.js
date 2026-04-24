function getFocusRequestFromQuery(search = window.location.search) {
   const params = new URLSearchParams(search);
   const species = params.get('focus')?.trim() ?? '';

   if (!species) {
      return null;
   }

   const exhibit = params.get('exhibit')?.trim() || null;

   return {
      species,
      exhibit,
   };
}

export function initFocusFromQuery({ onFocus } = {}) {
   const focusRequest = getFocusRequestFromQuery();

   if (!focusRequest || typeof onFocus !== 'function') {
      return;
   }

   onFocus(focusRequest);

   history.replaceState({}, '', window.location.pathname);
}
