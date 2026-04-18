import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { getLikelihoodPhrase } from '../../likelihood/likelihoodPresentation.js';

export const animalRenderer = {
   key: 'animal',

   isMatch(item, row) {
      const s1 = (item.species ?? item.SPECIES ?? '').trim();
      const s2 = (row.species ?? row.SPECIES ?? '').trim();
      if (!s1 || !s2 || s1 !== s2) return false;

      const e1 = (item.exhibit ?? item.EXHIBIT ?? '').trim();
      const e2 = (row.exhibit ?? row.EXHIBIT ?? '').trim();
      return e2 ? e1 === e2 : true;
   },

   createCard(a, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const exhibit = normalizeAssetKey(a.exhibit);
      const species = normalizeAssetKey(a.species);

      card.innerHTML = `
         <div class="tooltip-image-frame">
         <img
            src="images/animals/${exhibit}/${species}.png"
            alt="${a.species}"
            class="tooltip-image"
         >
         </div>

         <strong class="species-link"
         data-index="${index}"
         data-species="${a.species}"
         data-exhibit="${a.exhibit}"
         data-enclosure="${a.enclosure_type}">
         ${a.species}
         </strong>

         <span>Exhibit: ${a.exhibit}</span>
         <span>Enclosure Type: ${a.enclosure_type}</span>
         <span>Likelihood: ${getLikelihoodPhrase(a.likelihood)} (~${a.likelihood}%)</span>
      `;
      return card;
   },
};
