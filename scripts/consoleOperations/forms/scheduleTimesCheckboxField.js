import { asTrimmedStringList } from '../../api/normalizeValues.js';
import { APP_STRINGS } from '../../strings.js';

const SCHEDULE_TIMES_LIST_CLASS = 'console-operations-schedule-times-list';
const SCHEDULE_TIMES_PLACEHOLDER_CLASS = 'console-operations-schedule-times-placeholder';

export function resolveScheduleTimesListEl(el) {
   if (el?.classList?.contains(SCHEDULE_TIMES_LIST_CLASS)) {
      return el;
   }

   if (el?.id) {
      const byIdEl = document.getElementById(el.id);

      if (byIdEl?.classList?.contains(SCHEDULE_TIMES_LIST_CLASS)) {
         return byIdEl;
      }
   }

   const nestedEl = el?.querySelector?.(`.${SCHEDULE_TIMES_LIST_CLASS}`);

   if (nestedEl) {
      return nestedEl;
   }

   return document.getElementById('endWildEncounterScheduleTimes');
}

function getScheduleTimesListEl(el) {
   return resolveScheduleTimesListEl(el);
}

function renderScheduleTimesListMessage(listEl, message) {
   listEl.replaceChildren();

   const placeholderEl = document.createElement('div');
   placeholderEl.className = SCHEDULE_TIMES_PLACEHOLDER_CLASS;
   placeholderEl.textContent = message;
   listEl.appendChild(placeholderEl);
}

export function setScheduleTimesCheckboxListMessage(el, message) {
   const listEl = getScheduleTimesListEl(el);

   if (!listEl) {
      return;
   }

   renderScheduleTimesListMessage(listEl, message);
}

export function resetScheduleTimesCheckboxList(el) {
   const listEl = getScheduleTimesListEl(el);

   if (!listEl) {
      return;
   }

   renderScheduleTimesListMessage(
      listEl,
      APP_STRINGS.placeholders.selectWildEncounterFirst
   );
}

export function populateScheduleTimesCheckboxList(el, times = []) {
   const listEl = getScheduleTimesListEl(el);

   if (!listEl) {
      return;
   }

   const normalizedTimes = asTrimmedStringList(times);

   if (!normalizedTimes.length) {
      renderScheduleTimesListMessage(
         listEl,
         APP_STRINGS.help.noScheduledEncounterTimes
      );
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

export function updateScheduleTimesCheckboxList(el, {
   times = [],
   hasWildEncounter = false,
   hasDate = false,
} = {}) {
   const listEl = getScheduleTimesListEl(el);

   if (!listEl) {
      return;
   }

   const normalizedTimes = asTrimmedStringList(times);

   if (normalizedTimes.length) {
      populateScheduleTimesCheckboxList(listEl, normalizedTimes);
      return;
   }

   if (!hasWildEncounter) {
      resetScheduleTimesCheckboxList(listEl);
      return;
   }

   if (!hasDate) {
      setScheduleTimesCheckboxListMessage(
         listEl,
         APP_STRINGS.placeholders.selectDateFirst
      );
      return;
   }

   populateScheduleTimesCheckboxList(listEl, []);
}

export function clearScheduleTimesCheckboxList(el) {
   resetScheduleTimesCheckboxList(el);
}

export function getSelectedScheduleTimes(el) {
   const listEl = getScheduleTimesListEl(el);

   if (!listEl) {
      return [];
   }

   return [
      ...listEl.children,
   ]
      .flatMap((optionEl) =>
         [...optionEl.children].filter((child) => child.type === 'checkbox')
      )
      .filter((checkbox) => checkbox.checked)
      .map((checkbox) => checkbox.value.trim())
      .filter(Boolean);
}
