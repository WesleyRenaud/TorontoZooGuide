import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { getLikelihoodPhrase } from '../../likelihood/likelihoodPresentation.js';
import { createTooltipCard } from './cardFactory.js';

export const animalRenderer = {
   key: 'animal',

   isMatch(item, row) {
      const s1 = String(item?.species || '').trim();
      const s2 = String(row?.species || '').trim();
      if (!s1 || !s2 || s1 !== s2) return false;

      const e1 = String(item?.exhibit || '').trim();
      const e2 = String(row?.exhibit || '').trim();
      return e2 ? e1 === e2 : true;
   },

   createCard(a, index) {
      const exhibit = normalizeAssetKey(a.exhibit);
      const species = normalizeAssetKey(a.species);

      return createTooltipCard({
         index,
         image: {
            src: `images/animals/${exhibit}/${species}.png`,
            alt: a.species,
         },
         title: {
            text: a.species,
            className: 'species-link',
            dataset: {
               index,
               species: a.species,
               exhibit: a.exhibit,
               enclosure: a.enclosure_type,
            },
         },
         details: [
            `Exhibit: ${a.exhibit}`,
            `Enclosure Type: ${a.enclosure_type}`,
            `Likelihood: ${getLikelihoodPhrase(a.likelihood)} (~${a.likelihood}%)`,
         ],
      });
   },
};
