import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Status } from '../../shell/status.js';
import { Strings } from '../../../strings.js';

export class RemoveRestroomAlert {
   static createRemoveRestroomAlertController({
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
         return ControllerUtils.getFieldValue(restroomEl);
      }

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
      }

      async function show() {
         await ControllerUtils.loadOptionsAndShowPanel({
            statusEl,
            setStatus: Status.setStatus,
            loadOptions: Loaders.loadRestrooms,
            populateOptions: Dropdowns.populateRestroomDropdown,
            targetEl: restroomEl,
            resetForm,
            activatePanel,
            panelEl,
            errorMessage: Strings.loadErrors.restrooms,
         });
      }

      function hide() {
         ControllerUtils.hideConsolePanel({
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
            Status.setStatus(statusEl, Strings.validation.entityRequired(Strings.entityLabels.restroom), 'is-error');
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
            Status.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
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
}
