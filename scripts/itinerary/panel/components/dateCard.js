import { el } from '../dom.js';
import { getStoredItineraryDate } from '../../draftStorage.js';
import { formatISODateLong } from '../format.js';

export function makeDateCard(itin = {}) {
   const date = itin.date || getStoredItineraryDate();
   const prettyDate = formatISODateLong(date);

   if (!prettyDate) return null;

   const dateWrap = el('div', 'itin-panel-date');

   const topRow = el('div', 'itin-panel-date-top');
   const textWrap = el('div', 'itin-panel-date-text');

   textWrap.appendChild(el('div', 'itin-panel-date-label', 'Visit Date'));
   textWrap.appendChild(el('div', 'itin-panel-date-value', prettyDate));

   const actions = el('div', 'itin-panel-header-actions');

   const editBtn = el('button', 'itin-panel-section-edit-btn', 'Edit');
   editBtn.type = 'button';

   editBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      window.dispatchEvent(new CustomEvent('tzg:editItinerarySection', {
         detail: { step: 'date' }
      }));
   });

   actions.appendChild(editBtn);

   topRow.appendChild(textWrap);
   topRow.appendChild(actions);

   dateWrap.appendChild(topRow);

   return dateWrap;
}
