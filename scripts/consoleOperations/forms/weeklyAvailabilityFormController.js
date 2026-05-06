import { setStatus } from '../shell/status.js';
import { APP_STRINGS } from '../../strings.js';
import {
   hasCheckedField,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../helpers/controllerUtils.js';

export function createWeeklyAvailabilityFormController({
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
   entityLabel = APP_STRINGS.entityLabels.item,
   optionsLabel = APP_STRINGS.entityLabels.items,
   payloadKey = 'item',
   resultName = result => result?.[payloadKey] ?? '',
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
      resetFormFields([
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
      resetFormFields([entityEl, startDateEl, endDateEl, messageEl]);

      if (presetEl) {
         presetEl.value = 'everyDay';
      }

      resetDays();
      applyPreset();
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

   function hasAtLeastOneOpenDay() {
      return hasCheckedField([
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

   function isEveryDaySchedule() {
      return Boolean(
         mondayEl?.checked
         && tuesdayEl?.checked
         && wednesdayEl?.checked
         && thursdayEl?.checked
         && fridayEl?.checked
         && saturdayEl?.checked
         && sundayEl?.checked
      );
   }

   async function onShowClick() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus,
         loadOptions,
         populateOptions,
         targetEl: entityEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: APP_STRINGS.loadErrors.entityOptions(optionsLabel),
      });
   }

   async function onSubmitClick() {
      const entity = entityEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!entity) {
         setStatus(statusEl, APP_STRINGS.validation.entityRequired(entityLabel), 'is-error');
         return;
      }

      if (!hasAtLeastOneOpenDay()) {
         setStatus(statusEl, APP_STRINGS.validation.weeklyAvailability, 'is-error');
         return;
      }

      const dateError = validateOptionalDateRange(startDate, endDate);

      if (dateError) {
         setStatus(statusEl, dateError, 'is-error');
         return;
      }

      try {
         const result = await submitSchedule({
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
         });

         if (result.success) {
            const name = resultName(result) || entity;

            setStatus(
               statusEl,
               isEveryDaySchedule()
                  ? APP_STRINGS.status.open(name)
                  : APP_STRINGS.status.openingScheduleSaved(name),
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

   presetEl?.addEventListener('change', applyPreset);
   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
