import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class DrinkingFountainsOpen {
   static createDrinkingFountainsOpenController({
      showButtonEl,
      panelEl,
      submitButtonEl,
      statusEl,
      startDateEl,
      endDateEl,
      activatePanel,
   } = {}) {
      function resetForm() {
         ControllerUtils.resetFormFields([startDateEl, endDateEl]);
      }

      function show() {
         ConsoleStatusPresenter.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      async function onSubmitClick() {
         ConsoleStatusPresenter.setStatus(statusEl, '');

         const startDate = startDateEl?.value.trim() || '';
         const endDate = endDateEl?.value.trim() || '';
         const validationError = ControllerUtils.validateOptionalDateRange(startDate, endDate);

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsApi.setDrinkingFountainsOpen({
               startDate: startDate || null,
               endDate: endDate || null,
            });

            if (result.success) {
               ConsoleStatusPresenter.setStatus(statusEl, Strings.status.drinkingFountainsOpen, 'is-success');
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
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return { show };
   }
}
