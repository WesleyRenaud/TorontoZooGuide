import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalTooltipRenderer } from '../../../../scripts/tooltips/renderers/animalTooltipRenderer.js';
import { AnimalSelectorModel } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AssetKeyNormalizer } from '../../../../scripts/assets/assetKeyNormalizer.js';
import { CardFactory } from '../../../../scripts/tooltips/renderers/cardFactory.js';
import { LikelihoodPresenter } from '../../../../scripts/likelihood/likelihoodPresenter.js';
import { SpeciesLinkTitleBuilder } from '../../../../scripts/animals/speciesLinkTitleBuilder.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_IsMatch_TestSpeciesAndExhibit_ExpectMatchRules', () => {
   assert.equal(
      AnimalTooltipRenderer.isMatch(
         { species: 'Lion', exhibit: 'Savanna' },
         { species: 'Lion', exhibit: 'Savanna' }
      ),
      true
   );
   assert.equal(
      AnimalTooltipRenderer.isMatch(
         { species: 'Lion', exhibit: 'Savanna' },
         { species: 'Lion' }
      ),
      true
   );
   assert.equal(
      AnimalTooltipRenderer.isMatch(
         { species: 'Lion', exhibit: 'Savanna' },
         { species: 'Tiger', exhibit: 'Savanna' }
      ),
      false
   );
   assert.equal(
      AnimalTooltipRenderer.isMatch(
         { species: 'Lion', exhibit: 'Savanna' },
         { species: 'Lion', exhibit: 'Indo-Malaya' }
      ),
      false
   );
});

test('Test_CreateCard_TestAnimal_ExpectCardFactoryPayload', () => {
   const originalNormalize = AssetKeyNormalizer.normalize;
   const originalCreateCard = CardFactory.createTooltipCard;
   const originalTitle = SpeciesLinkTitleBuilder.createAnimalTitleLinkElement;
   const originalSpecies = AnimalSelectorModel.getAnimalSpecies;
   const originalEnclosure = AnimalSelectorModel.getAnimalEnclosureName;
   const originalSubtitle = AnimalSelectorModel.getAnimalSubtitle;
   const originalPhrase = LikelihoodPresenter.getLikelihoodPhrase;
   let captured;

   AssetKeyNormalizer.normalize = (value) => String(value).toLowerCase().replace(/\s+/g, '-');
   SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = (options) => ({ title: options });
   AnimalSelectorModel.getAnimalSpecies = () => 'African Lion';
   AnimalSelectorModel.getAnimalEnclosureName = () => 'Lion Enclosure';
   AnimalSelectorModel.getAnimalSubtitle = () => 'Africa Savanna';
   LikelihoodPresenter.getLikelihoodPhrase = () => 'High';
   CardFactory.createTooltipCard = (payload) => {
      captured = payload;
      return { card: true };
   };

   try {
      assert.equal(AnimalTooltipRenderer.key, 'animal');
      assert.deepEqual(
         AnimalTooltipRenderer.createCard({
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            enclosure_type: 'outdoor',
            likelihood: 85,
         }, 3),
         { card: true }
      );
      assert.equal(captured.index, 3);
      assert.equal(captured.image.src, 'images/details/animals/africa-savanna/african-lion.png');
      assert.equal(captured.image.alt, 'African Lion');
      assert.deepEqual(captured.details, [
         'Africa Savanna',
         Strings.tooltips.likelihoodDetail('High', 85),
      ]);
      assert.equal(captured.title.element.title.tagName, 'strong');
      assert.equal(captured.title.element.title.dataset.index, 3);
   } finally {
      AssetKeyNormalizer.normalize = originalNormalize;
      CardFactory.createTooltipCard = originalCreateCard;
      SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = originalTitle;
      AnimalSelectorModel.getAnimalSpecies = originalSpecies;
      AnimalSelectorModel.getAnimalEnclosureName = originalEnclosure;
      AnimalSelectorModel.getAnimalSubtitle = originalSubtitle;
      LikelihoodPresenter.getLikelihoodPhrase = originalPhrase;
   }
});
