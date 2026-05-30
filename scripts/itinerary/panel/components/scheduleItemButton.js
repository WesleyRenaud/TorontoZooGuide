import { el } from '../dom.js';

export function makeScheduleItemButton({
   label = 'Schedule item',
   onClick = null,
} = {}) {
   const row = el('div', 'itinerary-day-schedule-item-row');
   const button = el('button', 'itinerary-day-schedule-item-btn', label);
   button.type = 'button';

   if (typeof onClick === 'function') {
      button.addEventListener('click', onClick);
   }

   row.appendChild(button);

   return row;
}
