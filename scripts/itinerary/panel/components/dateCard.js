import { el } from '../dom.js';
import { getStoredItineraryDate } from '../../draftStorage.js';
import { Format } from '../format.js';
import { APP_STRINGS } from '../../../strings.js';

const { actions, selectors } = APP_STRINGS.itinerary;

export function makeDateCard(itin = {}) {
   const date = itin.date || getStoredItineraryDate();
   const prettyDate = Format.formatISODateLong(date);

   if (!prettyDate) return null;

   const dateWrap = el('div', 'itin-panel-date');

   const topRow = el('div', 'itin-panel-date-top');
   const textWrap = el('div', 'itin-panel-date-text');

   textWrap.appendChild(el('div', 'itin-panel-date-label', selectors.visitDate));
   textWrap.appendChild(el('div', 'itin-panel-date-value', prettyDate));

   const actionsWrap = el('div', 'itin-panel-header-actions');

   const editBtn = el('button', 'itin-panel-section-edit-btn', actions.edit);
   editBtn.type = 'button';

   editBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      window.dispatchEvent(new CustomEvent('tzg:editItinerarySection', {
         detail: { step: 'date' }
      }));
   });

   actionsWrap.appendChild(editBtn);

   topRow.appendChild(textWrap);
   topRow.appendChild(actionsWrap);

   dateWrap.appendChild(topRow);

   return dateWrap;
}
