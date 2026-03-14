import { loadRestaurants, postJson, setStatus, populateRestaurantDropdown } from './utils.js';

export function createRemoveRestaurantOpeningScheduleController({
   showButtonEl,
   panelEl,
   submitButtonEl,
   statusEl,
   restaurantEl,
   activatePanel,
   hidePanels
} = {}) {

   function resetForm() {
      if (restaurantEl) restaurantEl.value = '';
   }

   function hide() {
      panelEl?.classList.remove('active');
      setStatus(statusEl, '');
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

      setStatus(statusEl, '');

      if(!restaurant) {
         setStatus(statusEl, 'Restaurant is required.', 'is-error');
         return;
      }

      try {

         const result = await postJson('/remove-restaurant-opening-schedule', {
            restaurant
         });

         if(result.success) {

            setStatus(
               statusEl,
               `${result.restaurant} opening schedule was removed.`,
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
      hide
   };

}