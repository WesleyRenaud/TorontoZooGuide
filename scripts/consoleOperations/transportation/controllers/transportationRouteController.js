import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class TransportationRouteController {
   static createTransportationRouteController({
      showButtonEl,
      panelEl,
      submitButtonEl,
      statusEl,
      startDateEl,
      endDateEl,
      summerRouteEl,
      winterRouteEl,
      activatePanel,
   } = {}) {
      const formFieldEls = [startDateEl, endDateEl, summerRouteEl, winterRouteEl];


      function getSelectedRoute() {
         if (summerRouteEl?.checked) {
            return 'summer';
         }

         if (winterRouteEl?.checked) {
            return 'winter';
         }

         return '';
      }

      function getFormValues() {
         return {
            route: getSelectedRoute(),
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
         };
      }

      function validateForm({ route, startDate, endDate }) {
         if (!route) {
            return Strings.validation.entityRequired(Strings.labels.route);
         }

         return ControllerHelper.validateOptionalDateRange(startDate, endDate);
      }

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);

         if (summerRouteEl) {
            summerRouteEl.checked = true;
         }
      }

      function show() {
         ConsoleStatusPresenter.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      function hide() {
         ControllerHelper.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      async function submitRouteChange({ route, startDate, endDate }) {
         return ConsoleOperationsClient.setCurrentTransportationRoute({
            route,
            startDate: startDate || null,
            endDate: endDate || null,
         });
      }

      function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            Strings.status.transportationRouteSet(result),
            'is-success'
         );

         resetForm();
      }

      async function onSubmitClick() {
         const formValues = getFormValues();

         ConsoleStatusPresenter.setStatus(statusEl, '');

         const dateError = validateForm(formValues);

         if (dateError) {
            ConsoleStatusPresenter.setStatus(statusEl, dateError, 'is-error');
            return;
         }

         try {
            const result = await submitRouteChange(formValues);

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
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return {
         show,
         hide,
      };
   }
}
