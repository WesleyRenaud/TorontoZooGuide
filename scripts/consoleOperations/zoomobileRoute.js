import { postJson, setStatus } from './utils.js';

export function createZoomobileRouteController({
   showButtonEl,
   panelEl,
   submitButtonEl,
   statusEl,
   summerRouteEl,
   winterRouteEl,
   activatePanel,
   hidePanels
} = {}) {

   function resetForm() {
      if(summerRouteEl) summerRouteEl.checked = true;
      if(winterRouteEl) winterRouteEl.checked = false;
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

      if(summerRouteEl?.checked) {
         route = 'summer';
      }
      else if(winterRouteEl?.checked) {
         route = 'winter';
      }

      setStatus(statusEl, '');

      if(!route) {
         setStatus(statusEl, 'Zoomobile route is required.', 'is-error');
         return;
      }

      try {

         const result = await postJson('/set-current-zoomobile-route', {
            route
         });

         if(result.success) {

            setStatus(
               statusEl,
               `Zoomobile route was set to ${result.route}.`,
               'is-success'
            );
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