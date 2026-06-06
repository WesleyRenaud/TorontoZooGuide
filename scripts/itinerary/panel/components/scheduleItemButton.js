import { el } from '../dom.js';

export function makeScheduleItemButton({
   label = 'Schedule item',
   onClick = null,
   variant = 'primary',
} = {}) {
   const button = el('button', 'itinerary-day-schedule-item-btn', label);
   button.type = 'button';

   if (variant === 'secondary') {
      button.classList.add('itinerary-day-schedule-item-btn--secondary');
   }

   if (typeof onClick === 'function') {
      button.addEventListener('click', onClick);
   }

   return button;
}

export function makeScheduleActionsBar(buttons = []) {
   const bar = el('div', 'itinerary-day-schedule-actions');

   buttons.forEach((button) => {
      bar.appendChild(button);
   });

   return bar;
}
