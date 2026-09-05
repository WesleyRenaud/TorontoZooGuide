import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ConsoleDatePickers } from '../../../datePickers/consoleDatePickers.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { DayPlannerSchedule } from '../../../itinerary/panel/dayPlannerSchedule.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

function timePairIsOrdered(startTime, endTime) {
   const startMinutes = DayPlannerSchedule.parseClockTimeMinutes(startTime);
   const endMinutes = DayPlannerSchedule.parseClockTimeMinutes(endTime);

   return (
      startMinutes != null
      && endMinutes != null
      && startMinutes < endMinutes
   );
}

export class AttractionHoursSchedule {
   static createAttractionHoursScheduleController({
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
      loadAttractions = Loaders.loadAttractions,
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
            attraction: ControllerUtils.getFieldValue(attractionEl),
            scheduleStartDate: ControllerUtils.getFieldValue(startDateEl),
            scheduleEndDate: ControllerUtils.getFieldValue(endDateEl),
            weekdayStartTime: ControllerUtils.getFieldValue(weekdayStartTimeEl),
            weekdayEndTime: ControllerUtils.getFieldValue(weekdayEndTimeEl),
            weekendHolidayStartTime: ControllerUtils.getFieldValue(weekendHolidayStartTimeEl),
            weekendHolidayEndTime: ControllerUtils.getFieldValue(weekendHolidayEndTimeEl),
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

         return ControllerUtils.validateOptionalDateRange(
            values.scheduleStartDate,
            values.scheduleEndDate
         );
      }

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
      }

      function applyTimeBounds(bounds) {
         ConsoleDatePickers.applyScheduleTimePickerBounds(
            weekdayStartTimePicker,
            bounds?.weekday
         );
         ConsoleDatePickers.applyScheduleTimePickerBounds(
            weekdayEndTimePicker,
            bounds?.weekday
         );
         ConsoleDatePickers.applyScheduleTimePickerBounds(
            weekendHolidayStartTimePicker,
            bounds?.weekendHoliday
         );
         ConsoleDatePickers.applyScheduleTimePickerBounds(
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
         Status.setStatus(
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
         Status.setStatus(statusEl, '');

         try {
            const attractions = await loadAttractions();
            Dropdowns.populateAttractionDropdown(attractionEl, attractions);
            resetForm();
            await refreshTimeBounds();
            activatePanel?.(panelEl);
         }
         catch {
            Status.setStatus(
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
         ControllerUtils.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: Status.setStatus,
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
         Status.setStatus(
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
            Status.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         Status.setStatus(statusEl, '');

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

               Status.setStatus(
                  statusEl,
                  ApiErrorMessageResolver.resolveConsoleMutationError(resolved),
                  'is-error'
               );
               return;
            }

            Status.setStatus(
               statusEl,
               ApiErrorMessageResolver.resolveConsoleMutationError(result),
               'is-error'
            );
         }
         catch {
            Status.setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
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
}
