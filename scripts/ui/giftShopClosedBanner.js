export function createGiftShopClosedBanner() {
   let el = null;

   function ensure() {
      if (el) return el;

      el = document.createElement('div');
      el.className = 'off-display-closed-banner';
      el.style.display = 'none';

      el.innerHTML = `
         <div class="off-display-closed-icon">⚠</div>
         <div class="off-display-closed-text"></div>
         <button class="off-display-closed-close" type="button" aria-label="Close">×</button>
      `;

      el.addEventListener('click', (e) => e.stopPropagation());
      el.querySelector('.off-display-closed-close').addEventListener('click', (e) => {
         e.stopPropagation();
         hide();
      });

      document.body.appendChild(el);
      return el;
   }

   function hide() {
      if (!el) return;
      el.style.display = 'none';
   }

   function sync(giftShop) {
      const message = giftShop?.closed_message;

      if (!message) {
         hide();
         return;
      }

      const banner = ensure();
      banner.querySelector('.off-display-closed-text').innerHTML = message;
      banner.style.display = 'flex';
   }

   return { sync, hide };
}