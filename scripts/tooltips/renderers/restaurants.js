import { normalizeParameter } from '../../utils/normalize.js';

export const restaurantRenderer = {
   key: 'restaurant',

   createCard(r, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const name = r.name || 'Restaurant';
      const normalizedName = normalizeParameter(name);
      const imgSrc = `images/restaurants/${normalizedName}.png`;

      card.innerHTML = `
         <div class="tooltip-image-frame">
         <img
            src="${imgSrc}"
            alt="${name}"
            class="tooltip-image"
            onerror="this.onerror=null; this.src='images/generic-icons/restaurant.png';"
         >
         </div>

         <strong>${name}</strong>
         ${r.sub_location ? `<span>Location: ${r.sub_location}</span>` : r.location ? `<span>Location: ${r.location}</span>` : ''}
         ${r.description ? `<span>Description: ${r.description}</span>` : ''}       
         ${r.menu_link ? `<span>
                  <a 
                     href="${r.menu_link}" 
                     target="_blank" 
                     rel="noopener noreferrer"
                     class="tooltip-link restaurant-menu-link"
                  >
                     MENU
                  </a>
               </span>` 
            : ''
         }      `;
      return card;
   },
};