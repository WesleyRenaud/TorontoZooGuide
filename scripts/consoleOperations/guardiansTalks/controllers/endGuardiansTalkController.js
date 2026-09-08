import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { Strings } from '../../../strings.js';

export class EndGuardiansTalkController {
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
            ConsoleDropdownPopulator.populateGuardiansTalkDropdown(talkNameEl, []);
         }
         else if (talkNameEl) {
            talkNameEl.value = '';
         }
      }

      function validateSelection({ talk, location, times }) {
         if (!location) {
            return Strings.validation.entityRequired(Strings.labels.location);
         }

         if (!talk) {
            return Strings.validation.entityRequired(Strings.labels.talkName);
         }

         if (!times.length) {
            return Strings.validation.entityRequired(Strings.labels.talkTimes);
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
         return ConsoleOperationsClient.endGuardiansTalkSchedule({
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
            ControllerHelper.resetFormFields([locationEl]);
            resetTalkDropdown();
            scheduleTimesFilterController?.clear?.();
         },
         getSelectionValues: () => ({
            talk: ControllerHelper.getFieldValue(talkNameEl),
            location: ControllerHelper.getFieldValue(locationEl),
            times: getSelectedTimes(),
         }),
         validateSelection,
         prepareForm,
         loadErrorMessage: Strings.loadErrors.locations,
         submitEndSchedule,
         successMessage: result => Strings.status.guardiansTalkScheduleEnded(result),
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
