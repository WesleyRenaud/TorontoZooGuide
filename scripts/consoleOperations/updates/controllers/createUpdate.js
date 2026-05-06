import { createUpdate } from '../../../api/consoleOperationsApi.js';
import {
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export function createCreateUpdateController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   titleEl,
   descriptionEl,
   typeEl,
   startDateEl,
   endDateEl,
   activatePanel,
} = {}) {
   const formFieldEls = [titleEl, descriptionEl, typeEl, startDateEl, endDateEl];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function getFormValues() {
      return {
         title: getFieldValue(titleEl),
         description: getFieldValue(descriptionEl),
         type: getFieldValue(typeEl),
         startDate: getFieldValue(startDateEl),
         endDate: getFieldValue(endDateEl),
      };
   }

   function validateForm(values) {
      if (!values.title) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.title);
      if (!values.description) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.description);
      if (!values.type) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.type);

      return validateOptionalDateRange(values.startDate, values.endDate);
   }

   function resetForm() {
      resetFormFields(formFieldEls);
   }

   function show() {
      setStatus(statusEl, '');
      resetForm();
      activatePanel?.(panelEl);
   }

   function hide() {
      hideConsolePanel({ panelEl, statusEl, setStatus });
   }

   async function onSubmitClick() {
      const values = getFormValues();
      const validationError = validateForm(values);

      setStatus(statusEl, '');

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await createUpdate(values);

         if (result.success) {
            setStatus(
               statusEl,
               APP_STRINGS.status.updateCreated(result),
               'is-success'
            );
            resetForm();
         }
         else {
            setStatus(statusEl, result.error || APP_STRINGS.common.genericFailed, 'is-error');
         }
      }
      catch (err) {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', show);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return { show, hide };
}
