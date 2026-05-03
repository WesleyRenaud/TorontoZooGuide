import { endUpdate } from '../../../api/consoleOperationsApi.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { setStatus } from '../../shell/status.js';
import {
   getSelectedUpdateIdentity,
   loadActiveUpdates,
   populateUpdateDropdown,
} from './updateOptions.js';

export function createEndUpdateController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   updateEl,
   endDateEl,
   activatePanel,
} = {}) {
   const formFieldEls = [updateEl, endDateEl];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function resetForm() {
      resetFormFields(formFieldEls);
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

   function validateForm({ title, startDate }) {
      if (!title || !startDate) return 'Update is required.';
      return null;
   }

   async function onSubmitClick() {
      const values = {
         ...getSelectedUpdateIdentity(updateEl),
         endDate: getFieldValue(endDateEl),
      };
      const validationError = validateForm(values);

      setStatus(statusEl, '');

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await endUpdate(values);

         if (result.success) {
            setStatus(statusEl, 'Update was ended.', 'is-success');
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
