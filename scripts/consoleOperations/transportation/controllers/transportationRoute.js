import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

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
            return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.route);
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
         Status.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      function hide() {
         ControllerUtils.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: Status.setStatus,
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
         Status.setStatus(
            statusEl,
            APP_STRINGS.status.transportationRouteSet(result),
            'is-success'
         );

         resetForm();
      }

      async function onSubmitClick() {
         const formValues = getFormValues();

         Status.setStatus(statusEl, '');

         const dateError = validateForm(formValues);

         if (dateError) {
            Status.setStatus(statusEl, dateError, 'is-error');
            return;
         }

         try {
            const result = await submitRouteChange(formValues);

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
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return {
         show,
         hide,
      };
   }
}
