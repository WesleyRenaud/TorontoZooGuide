import { setGuardiansTalkSchedule } from '../../../api/consoleOperationsApi.js';
import {
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
      resetFormFields([locationEl]);
      if (sameTimeEveryDayModeEl) {
         sameTimeEveryDayModeEl.checked = true;
      }
      resetTalkDropdown();
      syncTimeModeFields();
   }

   function getFormValues() {
      const dailyTime = getOptionalFieldValue(dailyTimeEl);
      const sameTimeEveryDay = isSameTimeEveryDayMode();

      return {
         talk: getFieldValue(talkNameEl),
         location: getFieldValue(locationEl),
         startDate: getFieldValue(startDateEl),
         endDate: getFieldValue(endDateEl),
         mondayTime: sameTimeEveryDay ? dailyTime : getOptionalFieldValue(mondayTimeEl),
         tuesdayTime: sameTimeEveryDay ? dailyTime : getOptionalFieldValue(tuesdayTimeEl),
         wednesdayTime: sameTimeEveryDay ? dailyTime : getOptionalFieldValue(wednesdayTimeEl),
         thursdayTime: sameTimeEveryDay ? dailyTime : getOptionalFieldValue(thursdayTimeEl),
         fridayTime: sameTimeEveryDay ? dailyTime : getOptionalFieldValue(fridayTimeEl),
         saturdayTime: sameTimeEveryDay ? dailyTime : getOptionalFieldValue(saturdayTimeEl),
         sundayTime: sameTimeEveryDay ? dailyTime : getOptionalFieldValue(sundayTimeEl),
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
         }
         else {
            setStatus(statusEl, result.error || APP_STRINGS.common.genericFailed, 'is-error');
         }
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
