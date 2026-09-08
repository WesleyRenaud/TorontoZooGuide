import { FocusFromQueryHelpers } from './focusFromQueryHelpers.js';

export class FocusFromQuery {
   static initFocusFromQuery({ onFocus } = {}) {
      const focusRequest = FocusFromQueryHelpers.getFocusRequestFromQuery();

      if (!focusRequest || typeof onFocus !== 'function') {
         return;
      }

      onFocus(focusRequest);

      history.replaceState({}, '', window.location.pathname);
   }
}
