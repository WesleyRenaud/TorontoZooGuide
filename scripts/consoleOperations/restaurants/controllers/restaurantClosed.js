import { loadRestaurants, postJson, setStatus, populateRestaurantDropdown } from '../../utils.js';

export function createRestaurantClosedController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   restaurantEl,
   startDateEl,
   endDateEl,
   messageEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      if (restaurantEl) restaurantEl.value = '';
      if (startDateEl) startDateEl.value = '';
      if (endDateEl) endDateEl.value = '';
      if (messageEl) messageEl.value = '';
   }

   async function onShowClick() {

      setStatus(statusEl, '');

      try {
         const restaurants = await loadRestaurants();
         populateRestaurantDropdown(restaurantEl, restaurants);
         resetForm();
         activatePanel?.(panelEl);
      }
      catch(err) {
         setStatus(statusEl, 'Failed to load restaurants.', 'is-error');
         activatePanel?.(panelEl);
      }

   }

   async function onSubmitClick() {

      const restaurant = restaurantEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!restaurant) {
         setStatus(statusEl, 'Restaurant is required.', 'is-error');
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

         const result = await postJson('/set-restaurant-closed', {
            restaurant,
            startDate: startDate || null,
            endDate: endDate || null,
            message
         });

         if (result.success) {

            setStatus(
               statusEl,
               `${result.restaurant} was set as closed.`,
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
   cancelButtonEl?.addEventListener('click', hidePanels);
   submitButtonEl?.addEventListener('click', onSubmitClick);
}