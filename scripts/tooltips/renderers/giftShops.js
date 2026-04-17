import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';

export const giftShopRenderer = {
   key: 'giftShop',

   createCard(g, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const name = g.name || 'Gift Shop';
      const normalizedName = normalizeAssetKey(name);
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
         ${g.description ? `<span>Description: ${g.description}</span>` : ''}       
      `;
      return card;
   },
};
