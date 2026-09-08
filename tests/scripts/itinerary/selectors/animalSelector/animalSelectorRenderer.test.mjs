import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelectorRenderer } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorRenderer.js';
import { AnimalSelectorModel } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AnimalSelectorRendererHelper } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorRendererHelper.js';
import { SpeciesLinkTitleBuilder } from '../../../../../scripts/animals/speciesLinkTitleBuilder.js';
import { ResultRenderer } from '../../../../../scripts/itinerary/selectors/base/resultRenderer.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_RenderAnimalSelectorRowLeft_TestRow_ExpectSelectorContent', () => {
   const originalSpecies = AnimalSelectorModel.getAnimalSpecies;
   const originalSubtitle = AnimalSelectorModel.getAnimalSubtitle;
   const originalImage = AnimalSelectorModel.buildAnimalImageSrc;
   const originalEnclosure = AnimalSelectorModel.getAnimalEnclosureName;
   const originalLikelihood = AnimalSelectorModel.getAnimalLikelihoodLevel;
   const originalTitle = SpeciesLinkTitleBuilder.createAnimalTitleLinkElement;
   const originalWarning = AnimalSelectorRendererHelper.createLikelihoodWarning;
   const originalTextColumn = ResultRenderer.createSelectorTextColumn;
   const originalRowContent = ResultRenderer.createSelectorRowContent;

   AnimalSelectorModel.getAnimalSpecies = () => 'Lion';
   AnimalSelectorModel.getAnimalSubtitle = () => 'Savanna';
   AnimalSelectorModel.buildAnimalImageSrc = () => '/lion.png';
   AnimalSelectorModel.getAnimalEnclosureName = () => 'Yard';
   AnimalSelectorModel.getAnimalLikelihoodLevel = () => 'low';
   SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = () => {
      const el = document.createElement('a');
      el.textContent = 'Lion';
      return el;
   };
   AnimalSelectorRendererHelper.createLikelihoodWarning = () => {
      const el = document.createElement('span');
      el.className = 'warn';
      return el;
   };
   ResultRenderer.createSelectorTextColumn = ({ subtitle, titleNode }) => {
      const el = document.createElement('div');
      el.dataset.subtitle = subtitle;
      el.appendChild(titleNode);
      return el;
   };
   ResultRenderer.createSelectorRowContent = ({ imageSrc, imageAlt, textColumnEl }) => {
      const el = document.createElement('div');
      el.dataset.imageSrc = imageSrc;
      el.dataset.imageAlt = imageAlt;
      el.appendChild(textColumnEl);
      return el;
   };

   try {
      const content = AnimalSelectorRenderer.renderAnimalSelectorRowLeft({});
      assert.equal(content.dataset.imageSrc, '/lion.png');
      assert.equal(content.dataset.imageAlt, Strings.itinerary.itemPhoto('Lion'));
      assert.equal(content.querySelector('.warn').className, 'warn');
   } finally {
      AnimalSelectorModel.getAnimalSpecies = originalSpecies;
      AnimalSelectorModel.getAnimalSubtitle = originalSubtitle;
      AnimalSelectorModel.buildAnimalImageSrc = originalImage;
      AnimalSelectorModel.getAnimalEnclosureName = originalEnclosure;
      AnimalSelectorModel.getAnimalLikelihoodLevel = originalLikelihood;
      SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = originalTitle;
      AnimalSelectorRendererHelper.createLikelihoodWarning = originalWarning;
      ResultRenderer.createSelectorTextColumn = originalTextColumn;
      ResultRenderer.createSelectorRowContent = originalRowContent;
   }
});

test('Test_RenderIncludeOffDisplayToggle_TestChange_ExpectCallbacks', () => {
   const search = document.createElement('input');
   search.className = 'itin-search-input';
   const inserted = [];
   const bodyEl = {
      querySelector(selector) {
         return selector === '.itin-search-input' ? search : null;
      },
      insertBefore(node, reference) {
         inserted.push({ node, reference });
         return node;
      },
   };
   const changes = [];
   let reruns = 0;

   AnimalSelectorRenderer.renderIncludeOffDisplayToggle({
      bodyEl,
      rerunSearch: () => {
         reruns += 1;
      },
      onChange: (checked) => {
         changes.push(checked);
      },
   });

   assert.equal(inserted.length, 1);
   assert.equal(inserted[0].reference, search);
   assert.equal(inserted[0].node.className, 'itin-selector-toggle-wrap');

   const label = inserted[0].node.children[0];
   const checkbox = label.children[0];
   assert.equal(checkbox.type, 'checkbox');
   assert.equal(checkbox.checked, false);
   assert.equal(
      label.children[1].textContent,
      Strings.itinerary.selectors.includeOffDisplayAnimals
   );

   checkbox.checked = true;
   checkbox.listeners.change();
   assert.deepEqual(changes, [true]);
   assert.equal(reruns, 1);
});
