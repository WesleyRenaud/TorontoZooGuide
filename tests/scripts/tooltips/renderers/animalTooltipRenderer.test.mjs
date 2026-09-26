import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalTooltipRenderer } from '../../../../scripts/tooltips/renderers/animalTooltipRenderer.js';
import { AnimalSelectorModel } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AssetKeyNormalizer } from '../../../../scripts/assets/assetKeyNormalizer.js';
import { CardFactory } from '../../../../scripts/tooltips/renderers/cardFactory.js';
import { LikelihoodPresenter } from '../../../../scripts/likelihood/likelihoodPresenter.js';
import { SpeciesLinkTitleBuilder } from '../../../../scripts/animals/speciesLinkTitleBuilder.js';
import { Strings } from '../../../../scripts/strings.js';
import { ItemType } from '../../../../scripts/shared/enums/itemType.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

const africanLion = 'African Lion';
const africaSavanna = 'Africa Savanna';


function _stubCardFactory() {
   const originals = {
      normalize: AssetKeyNormalizer.normalize,
      createCard: CardFactory.createTooltipCard,
      title: SpeciesLinkTitleBuilder.createAnimalTitleLinkElement,
      species: AnimalSelectorModel.getAnimalSpecies,
      enclosure: AnimalSelectorModel.getAnimalEnclosureName,
      subtitle: AnimalSelectorModel.getAnimalSubtitle,
      phrase: LikelihoodPresenter.getLikelihoodPhrase,
   };
   const captured = {};

   AssetKeyNormalizer.normalize = (value) => String(value).toLowerCase().replace(/\s+/g, '-');
   SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = (options) => ({ title: options });
   CardFactory.createTooltipCard = (payload) => {
      captured.payload = payload;
      return { card: true };
   };

   return { originals, captured };
}


function _restoreCardFactory(originals) {
   AssetKeyNormalizer.normalize = originals.normalize;
   CardFactory.createTooltipCard = originals.createCard;
   SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = originals.title;
   AnimalSelectorModel.getAnimalSpecies = originals.species;
   AnimalSelectorModel.getAnimalEnclosureName = originals.enclosure;
   AnimalSelectorModel.getAnimalSubtitle = originals.subtitle;
   LikelihoodPresenter.getLikelihoodPhrase = originals.phrase;
}


test('Test_IsMatch_TestSameSpeciesAndExhibit_ExpectTrue', () => {
   const item = { species: africanLion, exhibit: africaSavanna };
   const row = { species: africanLion, exhibit: africaSavanna };

   const isMatch = AnimalTooltipRenderer.isMatch(item, row);

   assert.equal(isMatch, true);
});


test('Test_IsMatch_TestSpeciesOnlyRow_ExpectTrue', () => {
   const item = { species: africanLion, exhibit: africaSavanna };
   const row = { species: africanLion };

   const isMatch = AnimalTooltipRenderer.isMatch(item, row);

   assert.equal(isMatch, true);
});


test('Test_IsMatch_TestDifferentSpecies_ExpectFalse', () => {
   const item = { species: africanLion, exhibit: africaSavanna };
   const row = { species: 'Amur Tiger', exhibit: africaSavanna };

   const isMatch = AnimalTooltipRenderer.isMatch(item, row);

   assert.equal(isMatch, false);
});


test('Test_IsMatch_TestDifferentExhibit_ExpectFalse', () => {
   const item = { species: africanLion, exhibit: africaSavanna };
   const row = { species: africanLion, exhibit: 'Indo-Malaya' };

   const isMatch = AnimalTooltipRenderer.isMatch(item, row);

   assert.equal(isMatch, false);
});


test('Test_CreateCard_TestAnimal_ExpectCardFactoryPayload', () => {
   const { originals, captured } = _stubCardFactory();
   const species = africanLion;
   const exhibit = africaSavanna;
   const enclosure = 'Lion Enclosure';
   const likelihoodPhrase = 'High';
   const likelihood = 85;
   const index = 3;
   AnimalSelectorModel.getAnimalSpecies = () => species;
   AnimalSelectorModel.getAnimalEnclosureName = () => enclosure;
   AnimalSelectorModel.getAnimalSubtitle = () => exhibit;
   LikelihoodPresenter.getLikelihoodPhrase = () => likelihoodPhrase;

   try {
      const card = AnimalTooltipRenderer.createCard({
         species,
         exhibit,
         enclosure_type: 'outdoor',
         likelihood,
      }, index);

      assert.equal(AnimalTooltipRenderer.key, ItemType.ANIMAL);
      assert.deepEqual(card, { card: true });
      assert.equal(captured.payload.index, index);
      assert.equal(
         captured.payload.image.src,
         `images/details/animals/${AssetKeyNormalizer.normalize(exhibit)}/${AssetKeyNormalizer.normalize(species)}.png`
      );
      assert.equal(captured.payload.image.alt, species);
      assert.deepEqual(captured.payload.details, [
         exhibit,
         Strings.tooltips.likelihoodDetail(likelihoodPhrase, likelihood),
      ]);
      assert.equal(captured.payload.title.element.title.tagName, 'strong');
      assert.equal(captured.payload.title.element.title.dataset.index, index);
   } finally {
      _restoreCardFactory(originals);
   }
});


test('Test_CreateCard_TestTransportationOnlyAnimal_ExpectStandardDetails', () => {
   const { originals, captured } = _stubCardFactory();
   const species = 'Masai Giraffe';
   const exhibit = africaSavanna;
   const likelihoodPhrase = 'High';
   const likelihood = 85;
   AnimalSelectorModel.getAnimalSpecies = () => species;
   AnimalSelectorModel.getAnimalEnclosureName = () => 'Outdoor';
   AnimalSelectorModel.getAnimalSubtitle = () => exhibit;
   LikelihoodPresenter.getLikelihoodPhrase = () => likelihoodPhrase;

   try {
      AnimalTooltipRenderer.createCard({
         species,
         exhibit,
         likelihood,
         added_by_transportation: true,
         transportation: 'Zoomobile',
      }, 0);

      assert.deepEqual(captured.payload.details, [
         exhibit,
         Strings.tooltips.likelihoodDetail(likelihoodPhrase, likelihood),
      ]);
   } finally {
      _restoreCardFactory(originals);
   }
});
