import { editUpdate } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import {
   getFieldValue,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';
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
         errorMessage: APP_STRINGS.loadErrors.updates,
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
      if (!title || !startDate) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.update);
      if (!description) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.description);
      if (!type) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.type);

      if (endDate && new Date(endDate).getTime() < new Date(startDate).getTime()) {
         return APP_STRINGS.validation.endDateBeforeStartDate;
      }

      return null;
   }

   async function onSubmitClick() {
      const selectedUpdate = getSelectedUpdateData(updateEl);
      const values = {
         title: selectedUpdate.title,
         startDate: selectedUpdate.startDate,
         description: getFieldValue(descriptionEl),
         type: getFieldValue(typeEl),
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
            setStatus(statusEl, APP_STRINGS.status.updateEdited, 'is-success');
            resetForm();
         }
         else {
            setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
         }
      }
      catch (err) {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', show);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);
   updateEl?.addEventListener('change', populateFieldsFromSelectedUpdate);

   return { show, hide };
}
