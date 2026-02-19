import { normalizeParameter } from '../../utils/strings.js';
import { getPavilionName } from '../../utils/dom.js';

export const pavilionRenderer = {
   key: 'pavilion',

   isMatch(item, row) {
      const a = normalizeParameter(getPavilionName(item) || '');
      const b = normalizeParameter(getPavilionName(row) || '');
      return a && b && a === b;
   },

   createCard(p, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const name = getPavilionName(p) || 'Pavilion';
      const normalizedName = normalizeParameter(name);
      const imgSrc = `images/pavilions/${normalizedName}.png`;

      card.innerHTML = `
         <div class="tooltip-image-frame">
         <img
            src="${imgSrc}"
            alt="${name}"
            class="tooltip-image"
            onerror="this.onerror=null; this.src='images/generic-icons/pavilion.png';"
         >
         </div>

         <strong>${name}</strong>
         ${p.region ? `<span>Region: ${p.region}</span>` : ''}
         ${p.description ? `<span>Description: ${p.description}</span>` : ''}
      `;
      return card;
   },
};