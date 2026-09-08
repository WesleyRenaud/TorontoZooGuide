import assert from 'node:assert/strict';
import test from 'node:test';

import { ListView } from '../../../scripts/animals/listView.js';
import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';
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

test('Test_CreateAnimalsListView_TestRenderRegionsExhibitsAnimals_ExpectButtons', () => {
   const originalNormalize = AssetKeyNormalizer.normalize;
   AssetKeyNormalizer.normalize = (value) => String(value).toLowerCase().replace(/\s+/g, '-');

   try {
      const listEl = _createListEl();
      const view = ListView.createAnimalsListView({ listEl });
      const regionSelected = [];
      const exhibitSelected = [];
      const animalSelected = [];
      let backCalls = 0;

      view.renderRegions(
         [{ name: 'Africa' }],
         { onRegionSelected: (region) => { regionSelected.push(region); } }
      );
      assert.equal(listEl.children.length, 1);
      assert.equal(listEl.children[0].textContent, 'Africa');
      assert.equal(_imageSrc(listEl.children[0]), '../images/details/regions/africa.png');
      listEl.children[0].listeners.click();
      assert.deepEqual(regionSelected, [{ name: 'Africa' }]);

      view.renderExhibits(
         'Africa',
         ['Savanna'],
         {
            onBack: () => { backCalls += 1; },
            onExhibitSelected: (exhibit) => { exhibitSelected.push(exhibit); },
         }
      );
      assert.equal(listEl.children[0].textContent, Strings.animalsPage.back);
      assert.ok(listEl.children[0].classList.contains('back-button'));
      listEl.children[0].listeners.click();
      listEl.children[1].listeners.click();
      assert.equal(backCalls, 1);
      assert.deepEqual(exhibitSelected, ['Savanna']);

      view.renderAnimals(
         'Africa',
         'Savanna',
         ['Lion'],
         {
            onBack: () => { backCalls += 1; },
            onAnimalSelected: (animal) => { animalSelected.push(animal); },
         }
      );
      assert.equal(
         _imageSrc(listEl.children[1]),
         '../images/icons/animals/savanna/lion/lion.png'
      );
      listEl.children[1].listeners.click();
      assert.deepEqual(animalSelected, ['Lion']);

      view.clear();
      assert.equal(listEl.children.length, 0);
      assert.equal(listEl.scrollTop, 0);
   } finally {
      AssetKeyNormalizer.normalize = originalNormalize;
   }
});
