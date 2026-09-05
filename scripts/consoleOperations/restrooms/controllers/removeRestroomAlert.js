import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import {
   getFieldValue,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { populateRestroomDropdown } from '../../options/dropdowns.js';
import { loadRestrooms } from '../../options/loaders.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRemoveRestroomAlertController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   restroomEl,
   activatePanel,
} = {}) {
   const formFieldEls = [restroomEl];

   function getRestroom() {
      return getFieldValue(restroomEl);
   }

   function resetForm() {
      resetFormFields(formFieldEls);
   }

   async function show() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus: Status.setStatus,
         loadOptions: loadRestrooms,
         populateOptions: populateRestroomDropdown,
         targetEl: restroomEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: APP_STRINGS.loadErrors.restrooms,
      });
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus: Status.setStatus,
      });
   }

   function handleSubmitSuccess(result) {
      Status.setStatus(
         statusEl,
         `Alert removed for ${result.restroom}.`,
         'is-success'
      );

      resetForm();
   }

   async function onSubmitClick() {
      const restroom = getRestroom();

      Status.setStatus(statusEl, '');

      if (!restroom) {
         Status.setStatus(statusEl, APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.restroom), 'is-error');
         return;
      }

      try {
         const result = await ConsoleOperationsApi.removeRestroomAlert({ restroom });

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

   showButtonEl?.addEventListener('click', show);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
