import { editUpdate } from '../../../api/consoleOperationsApi.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { setStatus } from '../../shell/status.js';
import {
   getSelectedUpdateData,
   loadActiveUpdates,
   populateUpdateDropdown,
} from './updateOptions.js';

export function createEditUpdateController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   updateEl,
   descriptionEl,
   typeEl,
   endDateEl,
   activatePanel,
} = {}) {
   const formFieldEls = [updateEl, descriptionEl, typeEl, endDateEl];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function resetForm() {
      resetFormFields(formFieldEls);
   }

   function setFieldValue(fieldEl, value) {
      if (!fieldEl || !('value' in fieldEl)) {
         return;
      }

      fieldEl.value = value || '';
   }

   function populateFieldsFromSelectedUpdate() {
      const selectedUpdate = getSelectedUpdateData(updateEl);

      setFieldValue(descriptionEl, selectedUpdate.description);
      setFieldValue(typeEl, selectedUpdate.type);
      setFieldValue(endDateEl, selectedUpdate.endDate);
   }

   async function show() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus,
         loadOptions: loadActiveUpdates,
         populateOptions: populateUpdateDropdown,
         targetEl: updateEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: 'Failed to load updates.',
      });
   }

   function hide() {
      hideConsolePanel({ panelEl, statusEl, setStatus });
   }

   function validateForm({
      title,
      startDate,
      description,
      type,
      endDate,
   }) {
      if (!title || !startDate) return 'Update is required.';

      if (!description && !type && !endDate) {
         return 'Enter at least one change.';
      }

      if (endDate && new Date(endDate).getTime() < new Date(startDate).getTime()) {
         return 'End date cannot be before the start date.';
      }

      return null;
   }

   async function onSubmitClick() {
      const selectedUpdate = getSelectedUpdateData(updateEl);
      const values = {
         title: selectedUpdate.title,
         startDate: selectedUpdate.startDate,
         description: getFieldValue(descriptionEl) || null,
         type: getFieldValue(typeEl) || null,
         endDate: getFieldValue(endDateEl) || null,
      };
      const validationError = validateForm(values);

      setStatus(statusEl, '');

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await editUpdate(values);

         if (result.success) {
            setStatus(statusEl, 'Update was edited.', 'is-success');
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
   updateEl?.addEventListener('change', populateFieldsFromSelectedUpdate);

   return { show, hide };
}
