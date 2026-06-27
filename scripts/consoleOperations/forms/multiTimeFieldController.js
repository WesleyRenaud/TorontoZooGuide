import { APP_STRINGS } from '../../strings.js';
import { common } from '../../strings/common.js';
import { formatZooDisplayClockTime } from '../../visitDates/visitDateRules.js';

export function createMultiTimeFieldController({
   listEl,
   inputEl,
} = {}) {
   let times = [];

   function syncFieldState() {
      const fieldEl = inputEl?.closest('.console-operations-multi-time-field');

      if (fieldEl) {
         fieldEl.classList.toggle(
            'console-operations-multi-time-field--has-times',
            times.length > 0
         );
      }
   }

   function render() {
      if (!listEl) {
         return;
      }

      listEl.replaceChildren();

      times.forEach((time) => {
         const chipEl = document.createElement('div');
         chipEl.className = 'console-operations-time-chip';

         const labelEl = document.createElement('span');
         labelEl.className = 'console-operations-time-chip-label';
         labelEl.textContent = time;

         const removeButtonEl = document.createElement('button');
         removeButtonEl.type = 'button';
         removeButtonEl.className = 'console-operations-time-chip-remove';
         removeButtonEl.setAttribute(
            'aria-label',
            APP_STRINGS.help.removeScheduledTime(time)
         );
         removeButtonEl.textContent = common.closeSymbol;
         removeButtonEl.addEventListener('mousedown', (event) => {
            event.preventDefault();
         });
         removeButtonEl.addEventListener('click', () => {
            removeTime(time);
         });

         chipEl.append(labelEl, removeButtonEl);
         listEl.appendChild(chipEl);
      });

      syncFieldState();
   }

   function addTime(time) {
      const normalizedTime = formatZooDisplayClockTime(time?.trim() ?? '');

      if (!normalizedTime || times.includes(normalizedTime)) {
         return false;
      }

      times.push(normalizedTime);
      render();
      return true;
   }

   function removeTime(time) {
      times = times.filter(existingTime => existingTime !== time);
      render();
   }

   function removeLastTime() {
      if (times.length === 0) {
         return false;
      }

      times.pop();
      render();
      return true;
   }

   function getTimes() {
      return [...times];
   }

   function clearInput() {
      if (inputEl) {
         inputEl.value = '';
      }
   }

   function commitPendingInput() {
      const pendingTime = inputEl?.value?.trim() ?? '';

      if (!pendingTime) {
         return false;
      }

      const added = addTime(pendingTime);
      clearInput();
      return added;
   }

   function reset() {
      times = [];
      render();
      clearInput();
   }

   render();

   return {
      addTime,
      removeTime,
      removeLastTime,
      getTimes,
      commitPendingInput,
      reset,
   };
}
