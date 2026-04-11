import { normalizeParameter } from '../../utils/normalize.js';

export const attractionRenderer = {
   key: 'attraction',

   createCard(a, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const name = a.name || 'Attraction';
      const normalizedName = normalizeParameter(name);
      const imgSrc = `images/attractions/${normalizedName}.png`;

      card.innerHTML = `
         <div class="tooltip-image-frame">
         <img
            src="${imgSrc}"
            alt="${name}"
            class="tooltip-image"
            onerror="this.onerror=null; this.src='images/generic-icons/attraction.png';"
         >
         </div>

         <strong>${name}</strong>
         ${a.free_with_admission ? `<span>Free With Admission</span>` : `<span>Extra Charge</span>`}
         ${a.seasonal_schedule ? `<span>Seasonal Schedule: ${a.seasonal_schedule}</span>` : ''}
         ${a.description ? `<span>Description: ${a.description}</span>` : ''}       
         ${a.info_link ? `<span>
                  <a 
                     href="${a.info_link}" 
                     target="_blank" 
                     rel="noopener noreferrer"
                     class="tooltip-link gift-shop-link"
                  >
                     ${a.hyperlink_text}
                  </a>
               </span>`
            : ''
         }      `;
      return card;
   },
};
