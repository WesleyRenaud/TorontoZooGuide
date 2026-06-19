import {
   replaceGuardiansTalkScheduleOverlaps,
   setGuardiansTalkSchedule,
   trimGuardiansTalkScheduleOverlaps,
} from '../../../api/consoleOperationsApi.js';
import {
   OPENING_SCHEDULE_OVERLAP_RESOLUTION,
   resultHasOpeningScheduleOverlap,
} from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import {
   hasCheckedField,
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { populateGuardiansTalkDropdown } from '../../options/dropdowns.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

const TIME_MODE = {
   sameTimeEveryDay: 'sameTimeEveryDay',
   weekdayTimes: 'weekdayTimes',
};

export function createGuardiansTalkScheduleController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   talkNameEl,
   locationEl,
   startDateEl,
   endDateEl,
   sameTimeEveryDayModeEl,
   weekdayTimesModeEl,
   dailyTimeEl,
   mondayEl,
   tuesdayEl,
   wednesdayEl,
   thursdayEl,
   fridayEl,
   saturdayEl,
   sundayEl,
   mondayTimeEl,
   tuesdayTimeEl,
   wednesdayTimeEl,
   thursdayTimeEl,
   fridayTimeEl,
   saturdayTimeEl,
   sundayTimeEl,
   messageEl,
   activatePanel,
   talkLocationFilterController = null,
} = {}) {
   const dayCheckboxEls = [
      mondayEl,
      tuesdayEl,
      wednesdayEl,
      thursdayEl,
      fridayEl,
      saturdayEl,
      sundayEl,
   ];

   const timeFieldEls = [
      mondayTimeEl,
      tuesdayTimeEl,
      wednesdayTimeEl,
      thursdayTimeEl,
      fridayTimeEl,
      saturdayTimeEl,
      sundayTimeEl,
   ];

   const fieldEls = [
      startDateEl,
      endDateEl,
      dailyTimeEl,
      ...timeFieldEls,
      messageEl,
   ];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function getOptionalFieldValue(fieldEl) {
      const value = getFieldValue(fieldEl);
      return value || null;
   }

   function selectedTimeMode() {
      if (weekdayTimesModeEl?.checked) {
         return TIME_MODE.weekdayTimes;
      }

      return TIME_MODE.sameTimeEveryDay;
   }

   function isSameTimeEveryDayMode() {
      return selectedTimeMode() === TIME_MODE.sameTimeEveryDay;
   }

   function hasScheduledWeekday() {
      return timeFieldEls.some(fieldEl => Boolean(getFieldValue(fieldEl)));
   }

   function fieldWrapper(fieldEl) {
      return fieldEl?.closest('.console-operations-field') ?? null;
   }

   function setFieldVisible(fieldEl, isVisible) {
      const wrapper = fieldWrapper(fieldEl);

      if (wrapper) {
         wrapper.hidden = !isVisible;
      }
   }

   function syncTimeModeFields() {
      const sameTimeEveryDay = isSameTimeEveryDayMode();

      setFieldVisible(dailyTimeEl, sameTimeEveryDay);
      setFieldVisible(dayCheckboxEls[0], sameTimeEveryDay);
      timeFieldEls.forEach(fieldEl => setFieldVisible(fieldEl, !sameTimeEveryDay));
   }

   function resetTalkDropdown() {
      if (talkLocationFilterController?.clear) {
         talkLocationFilterController.clear();
         return;
      }

      if (talkNameEl?.tagName === 'SELECT') {
         populateGuardiansTalkDropdown(talkNameEl, []);
      }
      else if (talkNameEl) {
         talkNameEl.value = '';
      }
   }

   function resetForm() {
      resetFormFields(fieldEls);
      resetFormFields([locationEl, ...dayCheckboxEls]);
      if (sameTimeEveryDayModeEl) {
         sameTimeEveryDayModeEl.checked = true;
      }
      resetTalkDropdown();
      syncTimeModeFields();
   }

   function getWeekdayTime(dayCheckboxEl, weekdayTimeEl) {
      if (isSameTimeEveryDayMode()) {
         return dayCheckboxEl?.checked
            ? getOptionalFieldValue(dailyTimeEl)
            : null;
      }

      return getOptionalFieldValue(weekdayTimeEl);
   }

   function getFormValues() {
      return {
         talk: getFieldValue(talkNameEl),
         location: getFieldValue(locationEl),
         startDate: getFieldValue(startDateEl),
         endDate: getFieldValue(endDateEl),
         mondayTime: getWeekdayTime(mondayEl, mondayTimeEl),
         tuesdayTime: getWeekdayTime(tuesdayEl, tuesdayTimeEl),
         wednesdayTime: getWeekdayTime(wednesdayEl, wednesdayTimeEl),
         thursdayTime: getWeekdayTime(thursdayEl, thursdayTimeEl),
         fridayTime: getWeekdayTime(fridayEl, fridayTimeEl),
         saturdayTime: getWeekdayTime(saturdayEl, saturdayTimeEl),
         sundayTime: getWeekdayTime(sundayEl, sundayTimeEl),
         message: getFieldValue(messageEl),
      };
   }

   function validateForm(formValues) {
      if (!formValues.location) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.location);
      }

      if (!formValues.talk) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkName);
      }

      if (isSameTimeEveryDayMode() && !getFieldValue(dailyTimeEl)) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkTime);
      }

      if (isSameTimeEveryDayMode() && !hasCheckedField(dayCheckboxEls)) {
         return APP_STRINGS.validation.oneDay;
      }

      if (!isSameTimeEveryDayMode() && !hasScheduledWeekday()) {
         return APP_STRINGS.validation.oneDay;
      }

      return validateOptionalDateRange(
         formValues.startDate,
         formValues.endDate
      );
   }

   async function prepareForm() {
      if (talkLocationFilterController?.refreshLocations) {
         await talkLocationFilterController.refreshLocations();
      }
   }

   function show() {
      setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function onShowClick() {
      setStatus(statusEl, '');

      try {
         resetForm();
         await prepareForm();
         show();
      }
      catch(err) {
         setStatus(statusEl, APP_STRINGS.loadErrors.locations, 'is-error');
         show();
      }
   }

   async function onSubmitClick() {
      const formValues = getFormValues();

      setStatus(statusEl, '');

      const validationError = validateForm(formValues);

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await setGuardiansTalkSchedule(formValues);

         if (result.success) {
            setStatus(
               statusEl,
               APP_STRINGS.status.guardiansTalkScheduleSaved(result),
               'is-success'
            );
            resetForm();
            return;
         }

         if (resultHasOpeningScheduleOverlap(result)) {
            const resolution = await showOpeningScheduleOverlapDialog();

            if (resolution === OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
               const resolvedResult = await replaceGuardiansTalkScheduleOverlaps(formValues);

               if (resolvedResult?.success) {
                  setStatus(
                     statusEl,
                     APP_STRINGS.status.guardiansTalkScheduleSaved(resolvedResult),
                     'is-success'
                  );
                  resetForm();
                  return;
               }

               setStatus(
                  statusEl,
                  resolvedResult?.error || APP_STRINGS.common.genericFailed,
                  'is-error'
               );
               return;
            }

            if (resolution === OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
               const resolvedResult = await trimGuardiansTalkScheduleOverlaps(formValues);

               if (resolvedResult?.success) {
                  setStatus(
                     statusEl,
                     APP_STRINGS.status.guardiansTalkScheduleSaved(resolvedResult),
                     'is-success'
                  );
                  resetForm();
                  return;
               }

               setStatus(
                  statusEl,
                  resolvedResult?.error || APP_STRINGS.common.genericFailed,
                  'is-error'
               );
               return;
            }

            return;
         }

         setStatus(statusEl, result.error || APP_STRINGS.common.genericFailed, 'is-error');
      }
      catch(err) {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
      }
   }

   function onTimeModeChange(event) {
      if (event.target?.name !== 'guardiansTalkScheduleMode') {
         return;
      }

      syncTimeModeFields();
   }

   panelEl?.addEventListener('change', onTimeModeChange);
   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);
   syncTimeModeFields();

   return {
      show,
      hide,
   };
}
