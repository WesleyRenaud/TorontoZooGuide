import { ScheduleTimesCheckboxField } from './scheduleTimesCheckboxField.js';

export class ScheduleTimesCheckboxFieldRenderer {
   static SCHEDULE_TIMES_PLACEHOLDER_CLASS = 'console-operations-schedule-times-placeholder';
   static SCHEDULE_TIMES_SINGLE_CLASS = 'console-operations-schedule-times-single';

   static getScheduleTimesListEl(el) {
      return ScheduleTimesCheckboxField.resolveScheduleTimesListEl(el);
   }

   static renderScheduleTimesListMessage(listEl, message) {
      listEl.replaceChildren();

      const placeholderEl = document.createElement('div');
      placeholderEl.className = ScheduleTimesCheckboxFieldRenderer.SCHEDULE_TIMES_PLACEHOLDER_CLASS;
      placeholderEl.textContent = message;
      listEl.appendChild(placeholderEl);
   }

   static renderSingleSelectedScheduleTime(listEl, time) {
      listEl.replaceChildren();

      const timeEl = document.createElement('div');
      timeEl.className = ScheduleTimesCheckboxFieldRenderer.SCHEDULE_TIMES_SINGLE_CLASS;
      timeEl.dataset.scheduleTime = time;
      timeEl.textContent = time;
      listEl.appendChild(timeEl);
   }
}
