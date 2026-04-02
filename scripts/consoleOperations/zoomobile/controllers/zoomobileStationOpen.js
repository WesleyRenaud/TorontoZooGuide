import { loadZoomobileStations, setStatus, populateZoomobileStationDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

export function createZoomobileStationOpenController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   zoomobileStationEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      if (zoomobileStationEl) zoomobileStationEl.value = '';
   }

   function show() {
      setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      panelEl?.classList.remove('active');
      setStatus(statusEl, '');
   }

   async function onShowClick() {
      setStatus(statusEl, '');

      try {
         const zoomobileStations = await loadZoomobileStations();
         populateZoomobileStationDropdown(zoomobileStationEl, zoomobileStations);
         resetForm();
         setStatus(statusEl, '');
         activatePanel?.(panelEl);
      }
      catch(err) {
         setStatus(statusEl, 'Failed to load zoomobile stations.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {
      const zoomobileStation = zoomobileStationEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!zoomobileStation) {
         setStatus(statusEl, 'Zoomobile station is required.', 'is-error');
         return;
      }

      try {
         const result = await postJson('/set-zoomobile-station-open', {
            zoomobileStation
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.zoomobile_station} was set as open.`,
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
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}