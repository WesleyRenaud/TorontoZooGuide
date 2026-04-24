import { populateGuardiansTalkDropdown } from '../../options/dropdowns.js';
import { setGuardiansTalkSchedule } from '../../../api/consoleOperationsApi.js';
import {
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { createRecurringScheduleFormController } from '../../forms/recurringScheduleFormController.js';

export function createGuardiansTalkScheduleController({
   talkNameEl,
   locationEl,
   startDateEl,
   endDateEl,
   timeEl,
   mondayEl,
   tuesdayEl,
   wednesdayEl,
   thursdayEl,
   fridayEl,
   saturdayEl,
   sundayEl,
   messageEl,
   talkLocationFilterController = null,
   ...controllerOptions
} = {}) {
   const dayFieldEls = [
      mondayEl,
      tuesdayEl,
      wednesdayEl,
      thursdayEl,
      fridayEl,
      saturdayEl,
      sundayEl,
   ];

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

   function validateSelection({
      talk,
      location,
   }) {
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

   async function submitSchedule({
      talk,
      location,
      startDate,
      endDate,
      time,
      message,
   }) {
      return setGuardiansTalkSchedule({
         talk,
         location,
         startDate: startDate || null,
         endDate: endDate || null,
         time,
         monday: Boolean(mondayEl?.checked),
         tuesday: Boolean(tuesdayEl?.checked),
         wednesday: Boolean(wednesdayEl?.checked),
         thursday: Boolean(thursdayEl?.checked),
         friday: Boolean(fridayEl?.checked),
         saturday: Boolean(saturdayEl?.checked),
         sunday: Boolean(sundayEl?.checked),
         message,
      });
   }

   return createRecurringScheduleFormController({
      ...controllerOptions,
      startDateEl,
      endDateEl,
      timeEl,
      messageEl,
      dayFieldEls,
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
      submitSchedule,
      successMessage: result => `${result.talk} in ${result.location} schedule was saved.`,
      timeRequiredMessage: 'Talk time is required.',
   });
}
