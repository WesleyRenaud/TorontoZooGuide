import { populateGuardiansTalkDropdown } from '../../options/dropdowns.js';
import { endGuardiansTalkSchedule } from '../../../api/consoleOperationsApi.js';
import { resetFormFields } from '../../helpers/controllerUtils.js';
import { createEndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';

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
         return 'Location is required.';
      }

      if (!talk) {
         return 'Talk name is required.';
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
      loadErrorMessage: 'Failed to load locations.',
      submitEndSchedule,
      successMessage: result => `${result.talk} in ${result.location} schedule was ended.`,
   });
}
