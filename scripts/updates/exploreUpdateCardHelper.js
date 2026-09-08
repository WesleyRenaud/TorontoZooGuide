import { Strings } from '../strings.js';

export class ExploreUpdateCardHelper {
   static createUpdateTypeEl(update) {
      const typeEl = document.createElement('span');
      typeEl.className = `explore-update-type explore-update-type-${String(update.type || '')
         .toLowerCase()
         .replaceAll(' ', '-')}`;
      typeEl.textContent = update.type || Strings.labels.update;
      return typeEl;
   }
}
