import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { createEndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';
import { getSelectedScheduleTimes } from '../../forms/scheduleTimesCheckboxField.js';
import {
   getFieldValue,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { populateGuardiansTalkDropdown } from '../../options/dropdowns.js';
import { APP_STRINGS } from '../../../strings.js';

export function createEndGuardiansTalkScheduleController({
   talkNameEl,
   locationEl,
   timesEl,
   endDateEl,
   talkLocationFilterController = null,
   scheduleTimesFilterController = null,
   ...controllerOptions
} = {}) {

   function getSelectedTimes() {
      return getSelectedScheduleTimes(timesEl);
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

   const controller = createEndRecurringScheduleFormController({
      ...controllerOptions,
      endDateEl,
      resetSelection: () => {
         resetFormFields([locationEl]);
         resetTalkDropdown();
         scheduleTimesFilterController?.clear?.();
      },
      getSelectionValues: () => ({
         talk: getFieldValue(talkNameEl),
         location: getFieldValue(locationEl),
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
