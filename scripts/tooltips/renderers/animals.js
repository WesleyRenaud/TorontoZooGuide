import { CreateSpeciesLinkTitle } from '../../animals/createSpeciesLinkTitle.js';
import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { AnimalSelectorModel } from '../../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { LikelihoodPresentation } from '../../likelihood/likelihoodPresentation.js';
import { APP_STRINGS } from '../../strings.js';

export class Animals {
   static key = 'animal';

   static isMatch(item, row) {
      const s1 = ValueNormalizer.asTrimmedString(String(item?.species || ''));
      const s2 = ValueNormalizer.asTrimmedString(String(row?.species || ''));
      if (!s1 || !s2 || s1 !== s2) return false;

      const e1 = ValueNormalizer.asTrimmedString(String(item?.exhibit || ''));
      const e2 = ValueNormalizer.asTrimmedString(String(row?.exhibit || ''));
      return e2 ? e1 === e2 : true;
   }

   static createCard(a, index) {
      const exhibit = AssetKeyNormalizer.normalize(a.exhibit);
      const species = AssetKeyNormalizer.normalize(a.species);

      return CardFactory.createTooltipCard({
         index,
         image: {
            src: `images/details/animals/${exhibit}/${species}.png`,
            alt: a.species,
         },
         title: {
            element: CreateSpeciesLinkTitle.createAnimalTitleLinkElement({
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
   }
}
