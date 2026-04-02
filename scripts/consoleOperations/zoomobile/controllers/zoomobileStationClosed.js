import { loadZoomobileStations, setStatus, populateZoomobileStationDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

export function createZoomobileStationClosedController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   zoomobileStationEl,
   startDateEl,
   endDateEl,
   messageEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      if (zoomobileStationEl) zoomobileStationEl.value = '';
      if (startDateEl) startDateEl.value = '';
      if (endDateEl) endDateEl.value = '';
      if (messageEl) messageEl.value = '';
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
         activatePanel?.(panelEl);
      }
      catch (err) {

         setStatus(statusEl, 'Failed to load zoomobile stations.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {
      const zoomobileStation = zoomobileStationEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!zoomobileStation) {
         setStatus(statusEl, 'Zoomobile station is required.', 'is-error');
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
         const result = await postJson('/set-zoomobile-station-closed', {
            zoomobileStation,
            startDate: startDate || null,
            endDate: endDate || null,
            message
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.zoomobile_station} was set as closed.`,
               'is-success'
            );

            resetForm();
         }
         else {
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }
      }
      catch (err) {
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