import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { AttractionHoursScheduleHelper } from './attractionHoursScheduleHelper.js';
import { ConsoleDateFactory } from '../../../datePickers/consoleDateFactory.js';
import { OpeningScheduleChecker } from '../../forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapFragment } from '../../forms/openingScheduleOverlapFragment.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class AttractionHoursController {
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
      loadTimeBounds = ConsoleOperationsClient.getAttractionHoursScheduleTimeBounds,
      saveSchedule = ConsoleOperationsClient.setAttractionHoursSchedule,
      replaceScheduleOverlaps = ConsoleOperationsClient.replaceAttractionHoursScheduleOverlaps,
      trimScheduleOverlaps = ConsoleOperationsClient.trimAttractionHoursScheduleOverlaps,
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
            attraction: ControllerHelper.getFieldValue(attractionEl),
            scheduleStartDate: ControllerHelper.getFieldValue(startDateEl),
            scheduleEndDate: ControllerHelper.getFieldValue(endDateEl),
            weekdayStartTime: ControllerHelper.getFieldValue(weekdayStartTimeEl),
            weekdayEndTime: ControllerHelper.getFieldValue(weekdayEndTimeEl),
            weekendHolidayStartTime: ControllerHelper.getFieldValue(weekendHolidayStartTimeEl),
            weekendHolidayEndTime: ControllerHelper.getFieldValue(weekendHolidayEndTimeEl),
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

         if (!AttractionHoursScheduleHelper.timePairIsOrdered(values.weekdayStartTime, values.weekdayEndTime)) {
            return Strings.validation.attractionHoursWeekdayOrder;
         }

         if (!AttractionHoursScheduleHelper.timePairIsOrdered(
            values.weekendHolidayStartTime,
            values.weekendHolidayEndTime
         )) {
            return Strings.validation.attractionHoursWeekendHolidayOrder;
         }

         return ControllerHelper.validateOptionalDateRange(
            values.scheduleStartDate,
            values.scheduleEndDate
         );
      }

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
      }

      function applyTimeBounds(bounds) {
         ConsoleDateFactory.applyScheduleTimePickerBounds(
            weekdayStartTimePicker,
            bounds?.weekday
         );
         ConsoleDateFactory.applyScheduleTimePickerBounds(
            weekdayEndTimePicker,
            bounds?.weekday
         );
         ConsoleDateFactory.applyScheduleTimePickerBounds(
            weekendHolidayStartTimePicker,
            bounds?.weekendHoliday
         );
         ConsoleDateFactory.applyScheduleTimePickerBounds(
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
         ControllerHelper.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      async function resolveOverlapConflict(payload) {
         const resolution = await OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog();

         if (resolution === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
            return replaceScheduleOverlaps(payload);
         }

         if (resolution === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
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

            if (OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result)) {
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
