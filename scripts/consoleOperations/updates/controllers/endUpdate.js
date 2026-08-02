import { endUpdate } from '../../../api/consoleOperationsApi.js';
import {
   getFieldValue,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';
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
         errorMessage: APP_STRINGS.loadErrors.updates,
      });
   }

   function hide() {
      hideConsolePanel({ panelEl, statusEl, setStatus });
   }

   function validateForm({ title, startDate }) {
      if (!title || !startDate) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.update);
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
            setStatus(statusEl, APP_STRINGS.status.updateEnded, 'is-success');
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
