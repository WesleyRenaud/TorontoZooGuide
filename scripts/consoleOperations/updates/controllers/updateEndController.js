import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';
import { UpdateOptions } from './updateOptions.js';

export class UpdateEndController {
   static createEndUpdateController({
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
         ControllerHelper.resetFormFields(formFieldEls);
      }

      async function show() {
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions: UpdateOptions.loadActiveUpdates,
            populateOptions: UpdateOptions.populateUpdateDropdown,
            targetEl: updateEl,
            resetForm,
            activatePanel,
            panelEl,
            errorMessage: Strings.loadErrors.updates,
         });
      }

      function hide() {
         ControllerHelper.hideConsolePanel({ panelEl, statusEl, setStatus: ConsoleStatusPresenter.setStatus });
      }

      function validateForm({ title, startDate }) {
         if (!title || !startDate) return Strings.validation.entityRequired(Strings.labels.update);
         return null;
      }

      async function onSubmitClick() {
         const values = {
            ...getSelectedUpdateIdentity(updateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
         };
         const validationError = validateForm(values);

         ConsoleStatusPresenter.setStatus(statusEl, '');

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsClient.endUpdate(values);

            if (result.success) {
               ConsoleStatusPresenter.setStatus(statusEl, Strings.status.updateEnded, 'is-success');
               resetForm();
            }
            else {
               ConsoleStatusPresenter.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return { show, hide };
   }
}
