import { createUpdate } from '../../../api/consoleOperationsApi.js';
import {
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { setStatus } from '../../shell/status.js';

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
      if (!values.title) return 'Title is required.';
      if (!values.description) return 'Description is required.';
      if (!values.type) return 'Type is required.';

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
            setStatus(statusEl, `${result.title} was created.`, 'is-success');
            resetForm();
         }
         else {
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }
      }
      catch (err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', show);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return { show, hide };
}
