import { setStatus } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

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
      if (startDateEl) startDateEl.value = '';
      if (endDateEl) endDateEl.value = '';
      if (summerRouteEl) summerRouteEl.checked = true;
      if (winterRouteEl) winterRouteEl.checked = false;
   }

   function hide() {
      panelEl?.classList.remove('active');
      setStatus(statusEl, '');
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

      const effectiveStart = startDate || new Date().toISOString().split('T')[0];

      if (endDate) {
         const startMs = new Date(effectiveStart).getTime();
         const endMs = new Date(endDate).getTime();

         if (Number.isNaN(startMs) || Number.isNaN(endMs)) {
            setStatus(statusEl, 'Invalid start or end date.', 'is-error');
            return;
         }

         if (endMs < startMs) {
            setStatus(statusEl, 'End date cannot be before the start date.', 'is-error');
            return;
         }
      }

      try {

         const result = await postJson('/set-current-zoomobile-route', {
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
      resetForm
   };

}
