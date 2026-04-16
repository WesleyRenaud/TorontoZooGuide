import { loadRestaurants, setStatus, populateRestaurantDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../shared/controllerUtils.js';

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
      resetFormFields([restaurantEl, startDateEl, endDateEl, messageEl]);
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function onShowClick() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus,
         loadOptions: loadRestaurants,
         populateOptions: populateRestaurantDropdown,
         targetEl: restaurantEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: 'Failed to load restaurants.',
      });
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

      const dateError = validateOptionalDateRange(startDate, endDate);

      if (dateError) {
         setStatus(statusEl, dateError, 'is-error');
         return;
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
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      hide,
   };
}
