import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { applyScheduleTimePickerBounds } from '../../../datePickers/consoleDatePickers.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import {
   getFieldValue,
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { parseClockTimeMinutes } from '../../../itinerary/panel/dayPlannerSchedule.js';
import { populateAttractionDropdown } from '../../options/dropdowns.js';
import { loadAttractions as loadAttractionOptions } from '../../options/loaders.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

function timePairIsOrdered(startTime, endTime) {
   const startMinutes = parseClockTimeMinutes(startTime);
   const endMinutes = parseClockTimeMinutes(endTime);

   return (
      startMinutes != null
      && endMinutes != null
      && startMinutes < endMinutes
   );
}

export function createAttractionHoursScheduleController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   attractionEl,
   startDateEl,
   endDateEl,
   weekdayStartTimeEl,
   weekdayEndTimeEl,
   weekendHolidayStartTimeEl,
   weekendHolidayEndTimeEl,
   weekdayStartTimePicker = null,
   weekdayEndTimePicker = null,
   weekendHolidayStartTimePicker = null,
   weekendHolidayEndTimePicker = null,
   activatePanel,
   loadAttractions = loadAttractionOptions,
   loadTimeBounds = ConsoleOperationsApi.getAttractionHoursScheduleTimeBounds,
   saveSchedule = ConsoleOperationsApi.setAttractionHoursSchedule,
   replaceScheduleOverlaps = ConsoleOperationsApi.replaceAttractionHoursScheduleOverlaps,
   trimScheduleOverlaps = ConsoleOperationsApi.trimAttractionHoursScheduleOverlaps,
} = {}) {
   const formFieldEls = [
      attractionEl,
      startDateEl,
      endDateEl,
      weekdayStartTimeEl,
      weekdayEndTimeEl,
      weekendHolidayStartTimeEl,
      weekendHolidayEndTimeEl,
   ];

   function getFormValues() {
      return {
         attraction: getFieldValue(attractionEl),
         scheduleStartDate: getFieldValue(startDateEl),
         scheduleEndDate: getFieldValue(endDateEl),
         weekdayStartTime: getFieldValue(weekdayStartTimeEl),
         weekdayEndTime: getFieldValue(weekdayEndTimeEl),
         weekendHolidayStartTime: getFieldValue(weekendHolidayStartTimeEl),
         weekendHolidayEndTime: getFieldValue(weekendHolidayEndTimeEl),
      };
   }

   function validateForm(values) {
      if (!values.attraction) {
         return APP_STRINGS.validation.entityRequired(
            APP_STRINGS.entityLabels.attraction
         );
      }

      if (
         !values.weekdayStartTime
         || !values.weekdayEndTime
         || !values.weekendHolidayStartTime
         || !values.weekendHolidayEndTime
      ) {
         return APP_STRINGS.validation.attractionHoursTimesRequired;
      }

      if (!timePairIsOrdered(values.weekdayStartTime, values.weekdayEndTime)) {
         return APP_STRINGS.validation.attractionHoursWeekdayOrder;
      }

      if (!timePairIsOrdered(
         values.weekendHolidayStartTime,
         values.weekendHolidayEndTime
      )) {
         return APP_STRINGS.validation.attractionHoursWeekendHolidayOrder;
      }

      return validateOptionalDateRange(
         values.scheduleStartDate,
         values.scheduleEndDate
      );
   }

   function resetForm() {
      resetFormFields(formFieldEls);
   }

   function applyTimeBounds(bounds) {
      applyScheduleTimePickerBounds(
         weekdayStartTimePicker,
         bounds?.weekday
      );
      applyScheduleTimePickerBounds(
         weekdayEndTimePicker,
         bounds?.weekday
      );
      applyScheduleTimePickerBounds(
         weekendHolidayStartTimePicker,
         bounds?.weekendHoliday
      );
      applyScheduleTimePickerBounds(
         weekendHolidayEndTimePicker,
         bounds?.weekendHoliday
      );
   }

   async function refreshTimeBounds() {
      const values = getFormValues();
      const boundsResult = await loadTimeBounds({
         scheduleStartDate: values.scheduleStartDate,
         scheduleEndDate: values.scheduleEndDate,
      });

      if (boundsResult?.success) {
         applyTimeBounds({
            weekday: boundsResult.weekday,
            weekendHoliday: boundsResult.weekendHoliday,
         });
         return true;
      }

      applyTimeBounds(null);
      setStatus(
         statusEl,
         ApiErrorMessageResolver.resolveConsoleMutationError(
            boundsResult,
            APP_STRINGS.loadErrors.attractionHoursTimeBounds
         ),
         'is-error'
      );
      return false;
   }

   async function show() {
      setStatus(statusEl, '');

      try {
         const attractions = await loadAttractions();
         populateAttractionDropdown(attractionEl, attractions);
         resetForm();
         await refreshTimeBounds();
         activatePanel?.(panelEl);
      }
      catch {
         setStatus(
            statusEl,
            APP_STRINGS.loadErrors.entityOptions(
               APP_STRINGS.entityLabels.attractions
            ),
            'is-error'
         );
         activatePanel?.(panelEl);
      }
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function resolveOverlapConflict(payload) {
      const resolution = await showOpeningScheduleOverlapDialog();

      if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
         return replaceScheduleOverlaps(payload);
      }

      if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
         return trimScheduleOverlaps(payload);
      }

      return null;
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         APP_STRINGS.status.attractionHoursScheduleSaved(result.attraction),
         'is-success'
      );
      resetForm();
   }

   async function submit() {
      const values = getFormValues();
      const validationError = validateForm(values);

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      setStatus(statusEl, '');

      try {
         const result = await saveSchedule(values);

         if (result?.success) {
            handleSubmitSuccess(result);
            return;
         }

         if (OpeningScheduleOverlap.resultHasOpeningScheduleOverlap(result)) {
            const resolved = await resolveOverlapConflict(values);

            if (resolved?.success) {
               handleSubmitSuccess(resolved);
               return;
            }

            if (!resolved) {
               return;
            }

            setStatus(
               statusEl,
               ApiErrorMessageResolver.resolveConsoleMutationError(resolved),
               'is-error'
            );
            return;
         }

         setStatus(
            statusEl,
            ApiErrorMessageResolver.resolveConsoleMutationError(result),
            'is-error'
         );
      }
      catch {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', () => {
      void show();
   });
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', () => {
      void submit();
   });
   startDateEl?.addEventListener('change', () => {
      void refreshTimeBounds();
   });
   endDateEl?.addEventListener('change', () => {
      void refreshTimeBounds();
   });

   return {
      show,
      hide,
      submit,
      validateForm,
      getFormValues,
      refreshTimeBounds,
   };
}
