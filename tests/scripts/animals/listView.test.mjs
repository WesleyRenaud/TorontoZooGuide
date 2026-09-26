import assert from 'node:assert/strict';
import test from 'node:test';

import { ListView } from '../../../scripts/animals/listView.js';
import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


function _createListEl() {
   const listEl = document.createElement('div');
   Object.defineProperty(listEl, 'innerHTML', {
      configurable: true,
      get() {
         return listEl.children.length ? 'non-empty' : '';
      },
      set(value) {
         if (value === '') {
            listEl.replaceChildren();
         }
      },
   });
   listEl.scrollTop = 0;
   return listEl;
}


function _imageSrc(buttonEl) {
   const imageEl = [...buttonEl.children].find((child) => String(child.tagName).toLowerCase() === 'img');
   return imageEl?.src ?? null;
}


function _installNormalizeStub() {
   const originalNormalize = AssetKeyNormalizer.normalize;
   AssetKeyNormalizer.normalize = (value) => String(value).toLowerCase().replace(/\s+/g, '-');
   return originalNormalize;
}


test('Test_CreateAnimalsListView_TestRenderRegions_ExpectButtons', () => {
   const originalNormalize = _installNormalizeStub();
   const region = { name: 'Africa' };
   const regionSelected = [];

   try {
      const listEl = _createListEl();
      const view = ListView.createAnimalsListView({ listEl });

      view.renderRegions(
         [region],
         { onRegionSelected: (selected) => { regionSelected.push(selected); } }
      );
      const button = listEl.children.at(Position.FIRST);
      button.listeners.click();

      assert.equal(listEl.children.length, Position.SECOND);
      assert.equal(button.textContent, region.name);
      assert.equal(_imageSrc(button), `../images/details/regions/${AssetKeyNormalizer.normalize(region.name)}.png`);
      assert.deepEqual(regionSelected, [region]);
   } finally {
      AssetKeyNormalizer.normalize = originalNormalize;
   }
});


test('Test_CreateAnimalsListView_TestRenderExhibits_ExpectBackAndExhibit', () => {
   const originalNormalize = _installNormalizeStub();
   const regionName = 'Africa';
   const exhibit = 'Savanna';
   const exhibitSelected = [];
   let backCalls = Position.FIRST;

   try {
      const listEl = _createListEl();
      const view = ListView.createAnimalsListView({ listEl });

      view.renderExhibits(
         regionName,
         [exhibit],
         {
            onBack: () => { backCalls += 1; },
            onExhibitSelected: (selected) => { exhibitSelected.push(selected); },
         }
      );
      const backButton = listEl.children.at(Position.FIRST);
      const exhibitButton = listEl.children.at(Position.SECOND);
      backButton.listeners.click();
      exhibitButton.listeners.click();

      assert.equal(backButton.textContent, Strings.animalsPage.back);
      assert.ok(backButton.classList.contains('back-button'));
      assert.equal(backCalls, Position.SECOND);
      assert.deepEqual(exhibitSelected, [exhibit]);
   } finally {
      AssetKeyNormalizer.normalize = originalNormalize;
   }
});


test('Test_CreateAnimalsListView_TestRenderAnimals_ExpectAnimalButton', () => {
   const originalNormalize = _installNormalizeStub();
   const regionName = 'Africa';
   const exhibit = 'Savanna';
   const animal = 'Lion';
   const animalSelected = [];

   try {
      const listEl = _createListEl();
      const view = ListView.createAnimalsListView({ listEl });

      view.renderAnimals(
         regionName,
         exhibit,
         [animal],
         {
            onBack: () => {},
            onAnimalSelected: (selected) => { animalSelected.push(selected); },
         }
      );
      const animalButton = listEl.children.at(Position.SECOND);
      animalButton.listeners.click();

      assert.equal(
         _imageSrc(animalButton),
         `../images/icons/animals/${AssetKeyNormalizer.normalize(exhibit)}/${AssetKeyNormalizer.normalize(animal)}/${AssetKeyNormalizer.normalize(animal)}.png`
      );
      assert.deepEqual(animalSelected, [animal]);
   } finally {
      AssetKeyNormalizer.normalize = originalNormalize;
   }
});


test('Test_CreateAnimalsListView_TestClear_ExpectEmpty', () => {
   const originalNormalize = _installNormalizeStub();

   try {
      const listEl = _createListEl();
      const view = ListView.createAnimalsListView({ listEl });
      view.renderRegions([{ name: 'Africa' }], { onRegionSelected: () => {} });

      view.clear();

      assert.equal(listEl.children.length, 0);
      assert.equal(listEl.scrollTop, 0);
   } finally {
      AssetKeyNormalizer.normalize = originalNormalize;
   }
});
