import { SpeciesLinkTitleBuilder } from '../../animals/speciesLinkTitleBuilder.js';
import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { AnimalSelectorModel } from '../../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { LikelihoodPresenter } from '../../likelihood/likelihoodPresenter.js';
import { Strings } from '../../strings.js';

export class AnimalTooltipRenderer {
   static key = 'animal';

   static isMatch(item, row) {
      const s1 = ValueNormalizer.asTrimmedString(item?.species);
      const s2 = ValueNormalizer.asTrimmedString(row?.species);
      if (!s1 || !s2 || s1 !== s2) return false;

      const e1 = ValueNormalizer.asTrimmedString(item?.exhibit);
      const e2 = ValueNormalizer.asTrimmedString(row?.exhibit);
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
            element: SpeciesLinkTitleBuilder.createAnimalTitleLinkElement({
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
            Strings.tooltips.likelihoodDetail(
               LikelihoodPresenter.getLikelihoodPhrase(a.likelihood),
               a.likelihood
            ),
         ],
      });
   }
}
