import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class TransportationRoute {
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
            startDate: ControllerUtils.getFieldValue(startDateEl),
            endDate: ControllerUtils.getFieldValue(endDateEl),
         };
      }

      function validateForm({ route, startDate, endDate }) {
         if (!route) {
            return Strings.validation.entityRequired(Strings.labels.route);
         }

         return ControllerUtils.validateOptionalDateRange(startDate, endDate);
      }

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);

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
         ControllerUtils.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      async function submitRouteChange({ route, startDate, endDate }) {
         return ConsoleOperationsApi.setCurrentTransportationRoute({
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
