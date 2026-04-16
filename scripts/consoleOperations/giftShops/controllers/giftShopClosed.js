import { loadGiftShops, setStatus, populateGiftShopDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../shared/controllerUtils.js';

export function createGiftShopClosedController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   giftShopEl,
   startDateEl,
   endDateEl,
   messageEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      resetFormFields([giftShopEl, startDateEl, endDateEl, messageEl]);
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
         loadOptions: loadGiftShops,
         populateOptions: populateGiftShopDropdown,
         targetEl: giftShopEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: 'Failed to load gift shops.',
      });
   }

   async function onSubmitClick() {

      const giftShop = giftShopEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!giftShop) {
         setStatus(statusEl, 'Gift shop is required.', 'is-error');
         return;
      }

      const dateError = validateOptionalDateRange(startDate, endDate);

      if (dateError) {
         setStatus(statusEl, dateError, 'is-error');
         return;
      }

      try {

         const result = await postJson('/set-gift-shop-closed', {
            giftShop,
            startDate: startDate || null,
            endDate: endDate || null,
            message
         });

         if (result.success) {

            setStatus(
               statusEl,
               `${result.gift_shop} was set as closed.`,
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
