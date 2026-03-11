export function initFlatpickr( inputEl, options = {} ) {
   if ( !inputEl ) return null;

   try {
      const fpFn = window.flatpickr;

      if ( typeof fpFn !== 'function' ) {
         console.warn( '[flatpickr] window.flatpickr not available' );
         return null;
      }

      return fpFn( inputEl, {
         allowInput: true,
         clickOpens: true,
         monthSelectorType: 'static',
         ...options
      } );
   } catch ( err ) {
      console.error( '[flatpickr] init failed', err );
      return null;
   }
}