import { setStatus } from '../../shell/status.js';
import { setCurrentZoomobileRoute } from '../../../api/consoleOperationsApi.js';
import {
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';

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

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

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
         return 'Zoomobile route is required.';
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
         `Zoomobile route was set to ${result.route}.`,
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
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }
      }
      catch(err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', show);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
