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
   hidePanels
} = {}) {

   function resetForm() {
      resetFormFields([startDateEl, endDateEl, summerRouteEl, winterRouteEl]);

      if (summerRouteEl) {
         summerRouteEl.checked = true;
      }
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function onShowClick() {
      setStatus(statusEl, '');
      resetForm();
      activatePanel?.(panelEl);
   }

   async function onSubmitClick() {
      let route = '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';

      if (summerRouteEl?.checked) {
         route = 'summer';
      }
      else if (winterRouteEl?.checked) {
         route = 'winter';
      }

      setStatus(statusEl, '');

      if (!route) {
         setStatus(statusEl, 'Zoomobile route is required.', 'is-error');
         return;
      }

      const dateError = validateOptionalDateRange(startDate, endDate);

      if (dateError) {
         setStatus(statusEl, dateError, 'is-error');
         return;
      }

      try {

         const result = await setCurrentZoomobileRoute({
            route,
            startDate: startDate || null,
            endDate: endDate || null
         });

         if (result.success) {

            setStatus(
               statusEl,
               `Zoomobile route was set to ${result.route}.`,
               'is-success'
            );

            resetForm();
         }
         else {
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }

      }
      catch(err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', onShowClick);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      hide,
      resetForm,
   };
}
