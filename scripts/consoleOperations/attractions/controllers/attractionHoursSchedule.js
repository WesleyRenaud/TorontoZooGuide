import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { AttractionHoursScheduleHelpers } from './attractionHoursScheduleHelpers.js';
import { ConsoleDatePickers } from '../../../datePickers/consoleDatePickers.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { OpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

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
      loadAttractions = ConsoleOptionsLoader.loadAttractions,
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
            return Strings.validation.entityRequired(
               Strings.entityLabels.attraction
            );
         }

         if (
            !values.weekdayStartTime
            || !values.weekdayEndTime
            || !values.weekendHolidayStartTime
            || !values.weekendHolidayEndTime
         ) {
            return Strings.validation.attractionHoursTimesRequired;
         }

         if (!AttractionHoursScheduleHelpers.timePairIsOrdered(values.weekdayStartTime, values.weekdayEndTime)) {
            return Strings.validation.attractionHoursWeekdayOrder;
         }

         if (!AttractionHoursScheduleHelpers.timePairIsOrdered(
            values.weekendHolidayStartTime,
            values.weekendHolidayEndTime
         )) {
            return Strings.validation.attractionHoursWeekendHolidayOrder;
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
         ConsoleStatusPresenter.setStatus(
            statusEl,
            ApiErrorMessageResolver.resolveConsoleMutationError(
               boundsResult,
               Strings.loadErrors.attractionHoursTimeBounds
            ),
            'is-error'
         );
         return false;
      }

      async function show() {
         ConsoleStatusPresenter.setStatus(statusEl, '');

         try {
            const attractions = await loadAttractions();
            ConsoleDropdownPopulator.populateAttractionDropdown(attractionEl, attractions);
            resetForm();
            await refreshTimeBounds();
            activatePanel?.(panelEl);
         }
         catch {
            ConsoleStatusPresenter.setStatus(
               statusEl,
               Strings.loadErrors.entityOptions(
                  Strings.entityLabels.attractions
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
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      async function resolveOverlapConflict(payload) {
         const resolution = await OpeningScheduleOverlapDialog.showOpeningScheduleOverlapDialog();

         if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
            return replaceScheduleOverlaps(payload);
         }

         if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
            return trimScheduleOverlaps(payload);
         }

         return null;
      }

      function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            Strings.status.attractionHoursScheduleSaved(result.attraction),
            'is-success'
         );
         resetForm();
      }

      async function submit() {
         const values = getFormValues();
         const validationError = validateForm(values);

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         ConsoleStatusPresenter.setStatus(statusEl, '');

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

               ConsoleStatusPresenter.setStatus(
                  statusEl,
                  ApiErrorMessageResolver.resolveConsoleMutationError(resolved),
                  'is-error'
               );
               return;
            }

            ConsoleStatusPresenter.setStatus(
               statusEl,
               ApiErrorMessageResolver.resolveConsoleMutationError(result),
               'is-error'
            );
         }
         catch {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
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
