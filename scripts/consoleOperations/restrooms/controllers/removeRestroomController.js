import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class RemoveRestroomController {
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
         return ControllerHelper.getFieldValue(restroomEl);
      }

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
      }

      async function show() {
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions: ConsoleOptionsLoader.loadRestrooms,
            populateOptions: ConsoleDropdownPopulator.populateRestroomDropdown,
            targetEl: restroomEl,
            resetForm,
            activatePanel,
            panelEl,
            errorMessage: Strings.loadErrors.restrooms,
         });
      }

      function hide() {
         ControllerHelper.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            `Alert removed for ${result.restroom}.`,
            'is-success'
         );

         resetForm();
      }

      async function onSubmitClick() {
         const restroom = getRestroom();

         ConsoleStatusPresenter.setStatus(statusEl, '');

         if (!restroom) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.validation.entityRequired(Strings.entityLabels.restroom), 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsClient.removeRestroomAlert({ restroom });

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else {
               ConsoleStatusPresenter.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch(err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
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
