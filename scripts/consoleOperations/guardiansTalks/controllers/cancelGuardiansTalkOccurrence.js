import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import {
   getFieldValue,
   hideConsolePanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { populateGuardiansTalkDropdown } from '../../options/dropdowns.js';
import { JoinedTimesFormatter } from '../../../shared/joinedTimesFormatter.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export function createCancelGuardiansTalkOccurrenceController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   talkNameEl,
   locationEl,
   dateEl,
   timesEl,
   activatePanel,
   talkLocationFilterController = null,
   occurrenceFilterController = null,
} = {}) {
   const formFieldEls = [locationEl, dateEl];


   function getSelectedTimes() {
      return ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl);
   }

   function resetOccurrenceFields() {
      if (occurrenceFilterController?.clear) {
         occurrenceFilterController.clear();
      }
   }

   function resetTalkDropdown() {
      if (talkLocationFilterController?.clear) {
         talkLocationFilterController.clear();
      }
      else if (talkNameEl?.tagName === 'SELECT') {
         populateGuardiansTalkDropdown(talkNameEl, []);
      }
      else if (talkNameEl) {
         talkNameEl.value = '';
      }

      resetOccurrenceFields();
   }

   function resetForm() {
      resetFormFields(formFieldEls);
      resetTalkDropdown();
   }

   function getFormValues() {
      return {
         talk: getFieldValue(talkNameEl),
         location: getFieldValue(locationEl),
         date: getFieldValue(dateEl),
         times: getSelectedTimes(),
      };
   }

   function show() {
      Status.setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus: Status.setStatus,
      });
   }

   function validateForm({ talk, location, date, times }) {
      if (!location) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.location);
      }

      if (!talk) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkName);
      }

      if (!date) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.date);
      }

      if (!times.length) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkTimes);
      }

      return null;
   }

   async function refreshLocations() {
      if (talkLocationFilterController?.refreshLocations) {
         await talkLocationFilterController.refreshLocations();
      }
   }

   async function submitOccurrenceCancellation({ talk, location, date, times }) {
      return ConsoleOperationsApi.cancelGuardiansTalkOccurrence({
         talk,
         location,
         date,
         times,
      });
   }

   function handleSubmitSuccess(result) {
      Status.setStatus(
         statusEl,
         `${result.talk} in ${result.location} on ${result.date} at ${JoinedTimesFormatter.format(result.times)} was cancelled.`,
         'is-success'
      );

      resetForm();
   }

   async function onShowClick() {
      Status.setStatus(statusEl, '');

      try {
         resetForm();
         await refreshLocations();
         show();
      }
      catch(err) {
         Status.setStatus(statusEl, APP_STRINGS.loadErrors.locations, 'is-error');
         show();
      }
   }

   async function onSubmitClick() {
      const formValues = getFormValues();

      Status.setStatus(statusEl, '');

      const validationError = validateForm(formValues);

      if (validationError) {
         Status.setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await submitOccurrenceCancellation(formValues);

         if (result.success) {
            handleSubmitSuccess(result);
         }
         else {
            Status.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
         }

      }
      catch(err) {
         Status.setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
      }
   }

   locationEl?.addEventListener('change', () => {
      resetOccurrenceFields();
   });

   talkNameEl?.addEventListener('change', async () => {
      if (occurrenceFilterController?.refresh) {
         await occurrenceFilterController.refresh();
      }
      else {
         resetOccurrenceFields();
      }
   });

   dateEl?.addEventListener('change', () => {
      if (occurrenceFilterController?.refreshTimes) {
         occurrenceFilterController.refreshTimes();
      }
   });

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
