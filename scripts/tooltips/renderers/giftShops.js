import { normalizeParameter } from '../../utils/normalize.js';

export const giftShopRenderer = {
   key: 'giftShop',

   createCard(r, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const name = r.name || 'Gift Shop';
      const normalizedName = normalizeParameter(name);
      const imgSrc = `images/gift-shops/${normalizedName}.png`;

      card.innerHTML = `
         <div class="tooltip-image-frame">
         <img
            src="${imgSrc}"
            alt="${name}"
            class="tooltip-image"
            onerror="this.onerror=null; this.src='images/generic-icons/gift-shop.png';"
         >
         </div>

         <strong>${name}</strong>
         ${r.seasonal_schedule ? `<span>Seasonal Schedule: ${r.seasonal_schedule}</span>` : ''}
         ${r.description ? `<span>Description: ${r.description}</span>` : ''}       
      `;
      return card;
   },
};