import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { OpeningScheduleChecker } from './openingScheduleChecker.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
import { Strings } from '../../strings.js';

export class WeeklyAvailabilityFormController {
   static createWeeklyAvailabilityFormController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      entityEl,
      presetEl,
      startDateEl,
      endDateEl,
      mondayEl,
      tuesdayEl,
      wednesdayEl,
      thursdayEl,
      fridayEl,
      saturdayEl,
      sundayEl,
      holidaysOnlyEl,
      messageEl,
      activatePanel,
      loadOptions,
      populateOptions,
      submitSchedule,
      entityLabel = Strings.entityLabels.item,
      optionsLabel = Strings.entityLabels.items,
      payloadKey = 'item',
      resultName = result => result?.[payloadKey] ?? '',
      resolveOverlapConflict = null,
   } = {}) {

      function getDayCheckboxes() {
         return [
            mondayEl,
            tuesdayEl,
            wednesdayEl,
            thursdayEl,
            fridayEl,
            saturdayEl,
            sundayEl,
         ];
      }

      function resetDays() {
         ControllerHelper.resetFormFields([
            mondayEl,
            tuesdayEl,
            wednesdayEl,
            thursdayEl,
            fridayEl,
            saturdayEl,
            sundayEl,
            holidaysOnlyEl,
         ]);
      }

      function enableDayCheckboxes() {
         getDayCheckboxes().forEach(checkbox => {
            if (checkbox) checkbox.disabled = false;
         });

         if (holidaysOnlyEl) holidaysOnlyEl.disabled = false;
      }

      function applyPreset() {
         const preset = presetEl?.value ?? 'everyDay';

         resetDays();
         enableDayCheckboxes();

         if (preset === 'everyDay') {
            getDayCheckboxes().forEach(checkbox => {
               if (!checkbox) return;

               checkbox.checked = true;
               checkbox.disabled = true;
            });

            if (holidaysOnlyEl) {
               holidaysOnlyEl.checked = true;
               holidaysOnlyEl.disabled = true;
            }

            return;
         }

         if (preset === 'weekendsOnly') {
            if (saturdayEl) saturdayEl.checked = true;
            if (sundayEl) sundayEl.checked = true;

            getDayCheckboxes().forEach(checkbox => {
               if (checkbox) checkbox.disabled = true;
            });

            if (holidaysOnlyEl) {
               holidaysOnlyEl.checked = false;
               holidaysOnlyEl.disabled = true;
            }

            return;
         }

         if (preset === 'weekendsAndHolidays') {
            if (saturdayEl) saturdayEl.checked = true;
            if (sundayEl) sundayEl.checked = true;

            getDayCheckboxes().forEach(checkbox => {
               if (checkbox) checkbox.disabled = true;
            });

            if (holidaysOnlyEl) {
               holidaysOnlyEl.checked = true;
               holidaysOnlyEl.disabled = true;
            }
         }
      }

      function resetForm() {
         ControllerHelper.resetFormFields([entityEl, startDateEl, endDateEl, messageEl]);

         if (presetEl) {
            presetEl.value = 'everyDay';
         }

         resetDays();
         applyPreset();
      }

      function show() {
         ConsoleStatusPresenter.setStatus(statusEl, '');
         activatePanel?.(panelEl);
      }

      function hide() {
         ControllerHelper.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      function hasAtLeastOneOpenDay() {
         return ControllerHelper.hasCheckedField([
            mondayEl,
            tuesdayEl,
            wednesdayEl,
            thursdayEl,
            fridayEl,
            saturdayEl,
            sundayEl,
            holidaysOnlyEl,
         ]);
      }

      async function onShowClick() {
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions,
            populateOptions,
            targetEl: entityEl,
            resetForm,
            activatePanel,
            panelEl,
            errorMessage: Strings.loadErrors.entityOptions(optionsLabel),
         });
      }

      function buildPayload(entity, startDate, endDate, message) {
         return {
               [payloadKey]: entity,
               scheduleStartDate: startDate || null,
               scheduleEndDate: endDate || null,
               monday: Boolean(mondayEl?.checked),
               tuesday: Boolean(tuesdayEl?.checked),
               wednesday: Boolean(wednesdayEl?.checked),
               thursday: Boolean(thursdayEl?.checked),
               friday: Boolean(fridayEl?.checked),
               saturday: Boolean(saturdayEl?.checked),
               sunday: Boolean(sundayEl?.checked),
               holidaysOnly: Boolean(holidaysOnlyEl?.checked),
               message
         };
      }


      function handleSubmitSuccess(result, entity) {
         const name = resultName(result) || entity;

         ConsoleStatusPresenter.setStatus(
            statusEl,
            Strings.status.openingScheduleSaved(name),
            'is-success'
         );

         resetForm();
      }


      async function onSubmitClick() {
         const entity = ControllerHelper.getFieldValue(entityEl);
         const startDate = ControllerHelper.getFieldValue(startDateEl);
         const endDate = ControllerHelper.getFieldValue(endDateEl);
         const message = ControllerHelper.getFieldValue(messageEl);

         ConsoleStatusPresenter.setStatus(statusEl, '');

         if (!entity) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.validation.entityRequired(entityLabel), 'is-error');
            return;
         }

         if (!hasAtLeastOneOpenDay()) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.validation.weeklyAvailability, 'is-error');
            return;
         }

         const dateError = ControllerHelper.validateOptionalDateRange(startDate, endDate);

         if (dateError) {
            ConsoleStatusPresenter.setStatus(statusEl, dateError, 'is-error');
            return;
         }

         const payload = buildPayload(entity, startDate, endDate, message);

         try {
            const result = await submitSchedule(payload);

            if (result.success) {
               handleSubmitSuccess(result, entity);
               return;
            }

            if (OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result) && resolveOverlapConflict) {
               const resolvedResult = await resolveOverlapConflict(payload);

               if (resolvedResult?.success) {
                  handleSubmitSuccess(resolvedResult, entity);
                  return;
               }

               if (!resolvedResult) {
                  return;
               }

               ConsoleStatusPresenter.setStatus(
                  statusEl,
                  resolvedResult.error || Strings.common.genericFailed,
                  'is-error'
               );
               return;
            }

            ConsoleStatusPresenter.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
         }
         catch(err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      presetEl?.addEventListener('change', applyPreset);
      showButtonEl?.addEventListener('click', onShowClick);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return {
         show,
         hide,
      };
   }
}
