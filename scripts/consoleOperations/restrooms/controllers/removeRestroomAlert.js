import { removeRestroomAlert } from '../../../api/consoleOperationsApi.js';
import { APP_STRINGS } from '../../../strings.js';
import { loadRestrooms } from '../../options/loaders.js';
import { populateRestroomDropdown } from '../../options/dropdowns.js';
import { setStatus } from '../../shell/status.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';

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
      return restroomEl?.value.trim() ?? '';
   }

   function resetForm() {
      resetFormFields(formFieldEls);
   }

   async function show() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus,
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
         setStatus,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         `Alert removed for ${result.restroom}.`,
         'is-success'
      );

      resetForm();
   }

   async function onSubmitClick() {
      const restroom = getRestroom();

      setStatus(statusEl, '');

      if (!restroom) {
         setStatus(statusEl, APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.restroom), 'is-error');
         return;
      }

      try {
         const result = await removeRestroomAlert({ restroom });

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

   showButtonEl?.addEventListener('click', show);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
