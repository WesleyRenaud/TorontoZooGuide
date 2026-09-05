import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { APP_STRINGS } from '../../../strings.js';

export class EndGuardiansTalkSchedule {
   static createEndGuardiansTalkScheduleController({
      talkNameEl,
      locationEl,
      timesEl,
      endDateEl,
      talkLocationFilterController = null,
      scheduleTimesFilterController = null,
      ...controllerOptions
   } = {}) {

      function getSelectedTimes() {
         return ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl);
      }

      function resetTalkDropdown() {
         if (talkLocationFilterController?.clear) {
            talkLocationFilterController.clear();
            return;
         }

         if (talkNameEl?.tagName === 'SELECT') {
            Dropdowns.populateGuardiansTalkDropdown(talkNameEl, []);
         }
         else if (talkNameEl) {
            talkNameEl.value = '';
         }
      }

      function validateSelection({ talk, location, times }) {
         if (!location) {
            return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.location);
         }

         if (!talk) {
            return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkName);
         }

         if (!times.length) {
            return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkTimes);
         }

         return null;
      }

      async function prepareForm() {
         if (talkLocationFilterController?.refreshLocations) {
            await talkLocationFilterController.refreshLocations();
         }

         await scheduleTimesFilterController?.refresh?.();
      }

      async function submitEndSchedule({ talk, location, times, endDate }) {
         return ConsoleOperationsApi.endGuardiansTalkSchedule({
            talk,
            location,
            times,
            endDate: endDate || null,
         });
      }

      const controller = EndRecurringScheduleFormController.createEndRecurringScheduleFormController({
         ...controllerOptions,
         endDateEl,
         resetSelection: () => {
            ControllerUtils.resetFormFields([locationEl]);
            resetTalkDropdown();
            scheduleTimesFilterController?.clear?.();
         },
         getSelectionValues: () => ({
            talk: ControllerUtils.getFieldValue(talkNameEl),
            location: ControllerUtils.getFieldValue(locationEl),
            times: getSelectedTimes(),
         }),
         validateSelection,
         prepareForm,
         loadErrorMessage: APP_STRINGS.loadErrors.locations,
         submitEndSchedule,
         successMessage: result => APP_STRINGS.status.guardiansTalkScheduleEnded(result),
      });

      locationEl?.addEventListener('change', async () => {
         scheduleTimesFilterController?.clear?.();
      });

      talkNameEl?.addEventListener('change', async () => {
         scheduleTimesFilterController?.clear?.();
         await scheduleTimesFilterController?.refresh?.();
      });

      return controller;
   }
}
