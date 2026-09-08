import { FocusFromQueryHelper } from './focusFromQueryHelper.js';

export class FocusFromParser {
   static initFocusFromQuery({ onFocus } = {}) {
      const focusRequest = FocusFromQueryHelper.getFocusRequestFromQuery();

      if (!focusRequest || typeof onFocus !== 'function') {
         return;
      }

      onFocus(focusRequest);

      history.replaceState({}, '', window.location.pathname);
   }
}
