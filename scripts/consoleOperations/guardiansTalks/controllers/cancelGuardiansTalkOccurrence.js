import {
   populateGuardiansTalkDropdown,
} from '../../options/dropdowns.js';
import { APP_STRINGS } from '../../../strings.js';
import { setStatus } from '../../shell/status.js';
import {
   cancelGuardiansTalkOccurrence,
} from '../../../api/consoleOperationsApi.js';
import {
   hideConsolePanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';

export function createCancelGuardiansTalkOccurrenceController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   talkNameEl,
   locationEl,
   dateEl,
   timeEl,
   activatePanel,
   talkLocationFilterController = null,
   occurrenceFilterController = null,
} = {}) {
   const formFieldEls = [locationEl, talkNameEl, dateEl, timeEl];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function resetOccurrenceDropdowns() {
      if (occurrenceFilterController?.clear) {
         occurrenceFilterController.clear();
      }
      else {
         resetFormFields([dateEl, timeEl]);
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

      resetOccurrenceDropdowns();
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
         time: getFieldValue(timeEl),
      };
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

   function validateForm({ talk, location, date, time }) {
      if (!location) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.location);
      }

      if (!talk) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkName);
      }

      if (!date) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.date);
      }

      if (!time) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.time);
      }

      return null;
   }

   async function refreshLocations() {
      if (talkLocationFilterController?.refreshLocations) {
         await talkLocationFilterController.refreshLocations();
      }
   }

   async function submitOccurrenceCancellation({ talk, location, date, time }) {
      return cancelGuardiansTalkOccurrence({
         talk,
         location,
         date,
         time,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         `${result.talk} in ${result.location} on ${result.date} at ${result.time} was cancelled.`,
         'is-success'
      );

      resetForm();
   }

   async function onShowClick() {
      setStatus(statusEl, '');

      try {
         resetForm();
         await refreshLocations();
         show();
      }
      catch(err) {
         setStatus(statusEl, APP_STRINGS.loadErrors.locations, 'is-error');
         show();
      }
   }

   async function onSubmitClick() {
      const formValues = getFormValues();

      setStatus(statusEl, '');

      const validationError = validateForm(formValues);

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await submitOccurrenceCancellation(formValues);

         if (result.success) {
            handleSubmitSuccess(result);
         }
         else {
            setStatus(statusEl, result.error || APP_STRINGS.common.genericFailed, 'is-error');
         }

      }
      catch(err) {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
      }
   }

   locationEl?.addEventListener('change', () => {
      resetOccurrenceDropdowns();
   });

   talkNameEl?.addEventListener('change', async () => {
      if (occurrenceFilterController?.refresh) {
         await occurrenceFilterController.refresh();
      }
      else {
         resetOccurrenceDropdowns();
      }
   });

   dateEl?.addEventListener('change', () => {
      if (occurrenceFilterController?.refreshTimes) {
         occurrenceFilterController.refreshTimes();
      }
      else {
         resetFormFields([timeEl]);
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
