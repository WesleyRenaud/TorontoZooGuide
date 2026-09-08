import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class DrinkingFountainsOpenController {
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
         ControllerHelper.resetFormFields([startDateEl, endDateEl]);
      }

      function show() {
         ConsoleStatusPresenter.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      async function onSubmitClick() {
         ConsoleStatusPresenter.setStatus(statusEl, '');

         const startDate = ValueNormalizer.asTrimmedString(startDateEl?.value);
         const endDate = ValueNormalizer.asTrimmedString(endDateEl?.value);
         const validationError = ControllerHelper.validateOptionalDateRange(startDate, endDate);

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsClient.setDrinkingFountainsOpen({
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
