import { el } from '../dom.js';
import { APP_STRINGS } from '../../../strings.js';

const { scheduleItem } = APP_STRINGS.itinerary;

export function setScheduleItemButtonBusy(
   button,
   isBusy,
   busyLabel = scheduleItem.schedulingBusy
) {
   if (!button.dataset.defaultLabel) {
      button.dataset.defaultLabel = button.textContent;
   }

   button.disabled = isBusy;
   button.setAttribute('aria-busy', isBusy ? 'true' : 'false');
   button.classList.toggle('is-busy', isBusy);
   button.textContent = isBusy ? busyLabel : button.dataset.defaultLabel;
}

export async function runScheduleItemButtonAction(
   button,
   action,
   busyLabel = scheduleItem.schedulingBusy
) {
   if (button.disabled) {
      return;
   }

   setScheduleItemButtonBusy(button, true, busyLabel);

   try {
      await action();
   }
   finally {
      setScheduleItemButtonBusy(button, false);
   }
}

export function makeScheduleItemButton({
   label = scheduleItem.title,
   onClick = null,
   variant = 'primary',
} = {}) {
   const button = el('button', 'itinerary-day-schedule-item-btn', label);
   button.type = 'button';
   button.dataset.defaultLabel = label;

   if (variant === 'secondary') {
      button.classList.add('itinerary-day-schedule-item-btn--secondary');
   }

   if (variant === 'destructive') {
      button.classList.add('itinerary-day-schedule-item-btn--destructive');
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
