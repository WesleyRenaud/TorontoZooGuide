import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';

export const wildEncounterRenderer = {
   key: 'wildEncounter',

   createCard(w, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const name = w.name || 'Wild Encounter';
      const normalizedName = normalizeAssetKey(name);
      const imgSrc = `images/wild-encounters/${normalizedName}.png`;

      card.innerHTML = `
         <div class="tooltip-image-frame">
         <img
            src="${imgSrc}"
            alt="${name}"
            class="tooltip-image"
            onerror="this.onerror=null; this.src='images/generic-icons/wild-encounter.png';"
         >
         </div>

         <strong>${name}</strong>
         ${w.meeting_spot ?  `<span>${w.meeting_spot}</span>` : ''}
         ${w.time_of_day ? `<span>${w.time_of_day}</span>` : ''}
         ${w.link ? `<span>
                  <a 
                     href="${w.link}" 
                     target="_blank" 
                     rel="noopener noreferrer"
                     class="tooltip-link gift-shop-link"
                  >
                     More Info
                  </a>
               </span>`
            : ''
         }      `;
      return card;
   },
};
