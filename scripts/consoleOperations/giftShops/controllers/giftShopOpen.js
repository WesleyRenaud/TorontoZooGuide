import { loadGiftShops, setStatus, populateGiftShopDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

export function createGiftShopOpenController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   giftShopEl,
   activatePanel,
   hidePanels,
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

      if (!giftShop) {
         setStatus(statusEl, 'Gift shop is required.', 'is-error');
         return;
      }

      try {

         const result = await postJson('/set-gift-shop-open', {
            giftShop
         });

         if (result.success) {

            setStatus(
               statusEl,
               `${result.giftShop} was set as open.`,
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
      hide
   };

}