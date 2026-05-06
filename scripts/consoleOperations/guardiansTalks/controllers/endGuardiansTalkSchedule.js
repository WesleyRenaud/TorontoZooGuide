import { endGuardiansTalkSchedule } from '../../../api/consoleOperationsApi.js';
import { createEndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';
import { resetFormFields } from '../../helpers/controllerUtils.js';
import { populateGuardiansTalkDropdown } from '../../options/dropdowns.js';
import { APP_STRINGS } from '../../../strings.js';

export function createEndGuardiansTalkScheduleController({
   talkNameEl,
   locationEl,
   endDateEl,
   talkLocationFilterController = null,
   ...controllerOptions
} = {}) {
   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
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

   function validateSelection({ talk, location }) {
      if (!location) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.location);
      }

      if (!talk) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkName);
      }

      return null;
   }

   async function prepareForm() {
      if (talkLocationFilterController?.refreshLocations) {
         await talkLocationFilterController.refreshLocations();
      }
   }

   async function submitEndSchedule({ talk, location, endDate }) {
      return endGuardiansTalkSchedule({
         talk,
         location,
         endDate: endDate || null,
      });
   }

   return createEndRecurringScheduleFormController({
      ...controllerOptions,
      endDateEl,
      resetSelection: () => {
         resetFormFields([locationEl]);
         resetTalkDropdown();
      },
      getSelectionValues: () => ({
         talk: getFieldValue(talkNameEl),
         location: getFieldValue(locationEl),
      }),
      validateSelection,
      prepareForm,
      loadErrorMessage: APP_STRINGS.loadErrors.locations,
      submitEndSchedule,
      successMessage: result => APP_STRINGS.status.guardiansTalkScheduleEnded(result),
   });
}
