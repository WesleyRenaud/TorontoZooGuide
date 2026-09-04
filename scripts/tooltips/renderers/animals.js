import { createAnimalTitleLinkElement } from '../../animals/createSpeciesLinkTitle.js';
import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { createTooltipCard } from './cardFactory.js';
import { AnimalSelectorModel } from '../../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { LikelihoodPresentation } from '../../likelihood/likelihoodPresentation.js';
import { APP_STRINGS } from '../../strings.js';

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
      const exhibit = AssetKeyNormalizer.normalize(a.exhibit);
      const species = AssetKeyNormalizer.normalize(a.species);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/animals/${exhibit}/${species}.png`,
            alt: a.species,
         },
         title: {
            element: createAnimalTitleLinkElement({
               species: AnimalSelectorModel.getAnimalSpecies(a),
               enclosureName: AnimalSelectorModel.getAnimalEnclosureName(a),
               tagName: 'strong',
               className: 'tooltip-card-title',
               dataset: {
                  index,
                  species: a.species,
                  exhibit: a.exhibit,
                  enclosure: a.enclosure_type,
               },
            }),
         },
         details: [
            AnimalSelectorModel.getAnimalSubtitle(a),
            APP_STRINGS.tooltips.likelihoodDetail(
               LikelihoodPresentation.getLikelihoodPhrase(a.likelihood),
               a.likelihood
            ),
         ],
      });
   },
};
