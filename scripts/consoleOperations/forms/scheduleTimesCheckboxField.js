import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ScheduleTimesCheckboxFieldRenderer } from './scheduleTimesCheckboxFieldRenderer.js';
import { Strings } from '../../strings.js';

export class ScheduleTimesCheckboxField {
   static SCHEDULE_TIMES_LIST_CLASS = 'console-operations-schedule-times-list';

   static resolveScheduleTimesListEl(el) {
      if (el?.classList?.contains(ScheduleTimesCheckboxField.SCHEDULE_TIMES_LIST_CLASS)) {
         return el;
      }

      if (el?.id) {
         const byIdEl = document.getElementById(el.id);

         if (byIdEl?.classList?.contains(ScheduleTimesCheckboxField.SCHEDULE_TIMES_LIST_CLASS)) {
            return byIdEl;
         }
      }

      const nestedEl = el?.querySelector?.(`.${ScheduleTimesCheckboxField.SCHEDULE_TIMES_LIST_CLASS}`);

      if (nestedEl) {
         return nestedEl;
      }

      return document.getElementById('endWildEncounterScheduleTimes');
   }

   static setScheduleTimesCheckboxListMessage(el, message) {
      const listEl = ScheduleTimesCheckboxFieldRenderer.getScheduleTimesListEl(el);

      if (!listEl) {
         return;
      }

      ScheduleTimesCheckboxFieldRenderer.renderScheduleTimesListMessage(listEl, message);
   }

   static resetScheduleTimesCheckboxList(el) {
      const listEl = ScheduleTimesCheckboxFieldRenderer.getScheduleTimesListEl(el);

      if (!listEl) {
         return;
      }

      ScheduleTimesCheckboxFieldRenderer.renderScheduleTimesListMessage(
         listEl,
         Strings.placeholders.selectWildEncounterFirst
      );
   }

   static populateScheduleTimesCheckboxList(
      el,
      times = [],
      {
         autoSelectSingleTime = false,
      } = {}
   ) {
      const listEl = ScheduleTimesCheckboxFieldRenderer.getScheduleTimesListEl(el);

      if (!listEl) {
         return;
      }

      const normalizedTimes = ValueNormalizer.asTrimmedStringList(times);

      if (!normalizedTimes.length) {
         ScheduleTimesCheckboxFieldRenderer.renderScheduleTimesListMessage(
            listEl,
            Strings.help.noScheduledEncounterTimes
         );
         return;
      }

      if (autoSelectSingleTime && normalizedTimes.length === 1) {
         ScheduleTimesCheckboxFieldRenderer.renderSingleSelectedScheduleTime(listEl, normalizedTimes[0]);
         return;
      }

      const fragment = document.createDocumentFragment();

      normalizedTimes.forEach((time) => {
         const optionEl = document.createElement('label');
         optionEl.className = 'console-operations-checkbox-option';

         const checkboxEl = document.createElement('input');
         checkboxEl.type = 'checkbox';
         checkboxEl.value = time;
         checkboxEl.checked = false;

         optionEl.append(checkboxEl, ` ${time}`);
         fragment.appendChild(optionEl);
      });

      listEl.replaceChildren(fragment);
   }

   static updateScheduleTimesCheckboxList(el, {
      times = [],
      hasWildEncounter = false,
      hasDate = false,
      autoSelectSingleTime = false,
   } = {}) {
      const listEl = ScheduleTimesCheckboxFieldRenderer.getScheduleTimesListEl(el);

      if (!listEl) {
         return;
      }

      const normalizedTimes = ValueNormalizer.asTrimmedStringList(times);

      if (normalizedTimes.length) {
         ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(
            listEl,
            normalizedTimes,
            { autoSelectSingleTime }
         );
         return;
      }

      if (!hasWildEncounter) {
         ScheduleTimesCheckboxField.resetScheduleTimesCheckboxList(listEl);
         return;
      }

      if (!hasDate) {
         ScheduleTimesCheckboxField.setScheduleTimesCheckboxListMessage(
            listEl,
            Strings.placeholders.selectDateFirst
         );
         return;
      }

      ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, [], {
         autoSelectSingleTime,
      });
   }

   static clearScheduleTimesCheckboxList(el) {
      ScheduleTimesCheckboxField.resetScheduleTimesCheckboxList(el);
   }

   static getSelectedScheduleTimes(el) {
      const listEl = ScheduleTimesCheckboxFieldRenderer.getScheduleTimesListEl(el);

      if (!listEl) {
         return [];
      }

      const singleTimeEl = listEl.querySelector(`.${ScheduleTimesCheckboxFieldRenderer.SCHEDULE_TIMES_SINGLE_CLASS}`);
      const singleTime = ValueNormalizer.asTrimmedString(
         singleTimeEl?.dataset?.scheduleTime
      );

      if (singleTime) {
         return [singleTime];
      }

      return [
         ...listEl.children,
      ]
         .flatMap((optionEl) =>
            [...optionEl.children].filter((child) => child.type === 'checkbox')
         )
         .filter((checkbox) => checkbox.checked)
         .map((checkbox) => ValueNormalizer.asTrimmedString(checkbox.value))
         .filter(Boolean);
   }
}
