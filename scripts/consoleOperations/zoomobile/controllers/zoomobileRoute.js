import { setCurrentZoomobileRoute } from '../../../api/consoleOperationsApi.js';
import {
   getFieldValue,
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export function createZoomobileRouteController({
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
         startDate: getFieldValue(startDateEl),
         endDate: getFieldValue(endDateEl),
      };
   }

   function validateForm({ route, startDate, endDate }) {
      if (!route) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.map.zoomobileRoute.title);
      }

      return validateOptionalDateRange(startDate, endDate);
   }

   function resetForm() {
      resetFormFields(formFieldEls);

      if (summerRouteEl) {
         summerRouteEl.checked = true;
      }
   }

   function show() {
      setStatus(statusEl, '');
      resetForm();
      activatePanel?.(panelEl);
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function submitRouteChange({ route, startDate, endDate }) {
      return setCurrentZoomobileRoute({
         route,
         startDate: startDate || null,
         endDate: endDate || null,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         APP_STRINGS.status.zoomobileRouteSet(result),
         'is-success'
      );

      resetForm();
   }

   async function onSubmitClick() {
      const formValues = getFormValues();

      setStatus(statusEl, '');

      const dateError = validateForm(formValues);

      if (dateError) {
         setStatus(statusEl, dateError, 'is-error');
         return;
      }

      try {
         const result = await submitRouteChange(formValues);

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
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
