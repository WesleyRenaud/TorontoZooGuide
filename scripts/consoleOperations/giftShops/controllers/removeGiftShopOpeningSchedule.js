import { loadGiftShops, postJson, setStatus, populateGiftShopDropdown } from '../../utils.js';

export function createRemoveGiftShopOpeningScheduleController({
   showButtonEl,
   panelEl,
   submitButtonEl,
   statusEl,
   giftShopEl,
   activatePanel,
   hidePanels
} = {}) {

   function resetForm() {
      if (giftShopEl) giftShopEl.value = '';
   }

   function hide() {
      panelEl?.classList.remove('active');
      setStatus(statusEl, '');
   }

   async function onShowClick() {
      setStatus(statusEl, '');

      try {
         const giftShops = await loadGiftShops();
         populateGiftShopDropdown(giftShopEl, giftShops);
         resetForm();
         activatePanel?.(panelEl);
      }
      catch(err) {
         setStatus(statusEl, 'Failed to load gift shops.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {

      const giftShop = giftShopEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if(!giftShop) {
         setStatus(statusEl, 'Gift shop is required.', 'is-error');
         return;
      }

      try {

         const result = await postJson('/remove-gift-shop-opening-schedule', {
            giftShop
         });

         if(result.success) {

            setStatus(
               statusEl,
               `${result.giftShop} opening schedule was removed.`,
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