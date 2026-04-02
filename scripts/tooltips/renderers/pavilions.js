import { normalizeParameter } from '../../utils/normalize.js';

export const pavilionRenderer = {
   key: 'pavilion',

   createCard(p, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const name = p.name || 'Pavilion';
      const normalizedName = normalizeParameter(name);
      const imgSrc = `images/pavilions/${normalizedName}.png`;

      card.innerHTML = `
         <div class="tooltip-image-frame">
         <img
            src="${imgSrc}"
            alt="${name}"
            class="tooltip-image"
            onerror="this.onerror=null; this.src='images/generic-icons/pavilion-open.png';"
         >
         </div>

         <strong>${name}</strong>
         ${p.region ? `<span>Region: ${p.region}</span>` : ''}
         ${p.description ? `<span>Description: ${p.description}</span>` : ''}
      `;
      return card;
   },
};