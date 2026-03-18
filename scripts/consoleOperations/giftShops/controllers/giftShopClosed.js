import { loadGiftShops, postJson, setStatus, populateGiftShopDropdown } from '../../utils.js';

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
      if(giftShopEl) giftShopEl.value = '';
      if(startDateEl) startDateEl.value = '';
      if(endDateEl) endDateEl.value = '';
      if(messageEl) messageEl.value = '';
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
         console.log(err);
         setStatus(statusEl, 'Failed to load gift shops.', 'is-error');
         activatePanel?.(panelEl);
      }

   }

   async function onSubmitClick() {

      const giftShop = giftShopEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if(!giftShop) {
         setStatus(statusEl, 'Gift shop is required.', 'is-error');
         return;
      }

      const effectiveStart = startDate || new Date().toISOString().split('T')[0];

      if(endDate) {

         const startMs = new Date(effectiveStart).getTime();
         const endMs = new Date(endDate).getTime();

         if(Number.isNaN(startMs) || Number.isNaN(endMs)) {
            setStatus(statusEl, 'Invalid start or end date.', 'is-error');
            return;
         }

         if(endMs < startMs) {
            setStatus(statusEl, 'End date cannot be before the start date.', 'is-error');
            return;
         }

      }

      try {

         const result = await postJson('/set-gift-shop-closed', {
            giftShop,
            startDate: startDate || null,
            endDate: endDate || null,
            message
         });

         if(result.success) {

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
   cancelButtonEl?.addEventListener('click', hidePanels);
   submitButtonEl?.addEventListener('click', onSubmitClick);
}