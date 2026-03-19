import { el } from '../dom.js';
import { DATE_KEY } from '../storage.js';
import { formatISODateLong } from '../format.js';

export function makeDateCard(itin = {}) {
   const dateISO = itin.dateISO || localStorage.getItem(DATE_KEY) || '';
   const prettyDate = formatISODateLong(dateISO);

   if (!prettyDate) return null;

   const dateWrap = el('div', 'itin-panel-date');
   dateWrap.appendChild(el('div', 'itin-panel-date-label', 'Visit Date'));
   dateWrap.appendChild(el('div', 'itin-panel-date-value', prettyDate));
   return dateWrap;
}