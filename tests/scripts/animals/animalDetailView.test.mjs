import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalDetailView } from '../../../scripts/animals/animalDetailView.js';
import { AnimalDetailViewBuilder } from '../../../scripts/animals/animalDetailViewBuilder.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateAnimalDetailView_TestRender_ExpectContent', () => {
   const listEl = document.createElement('div');
   listEl.scrollTop = 20;
   const originalBack = AnimalDetailViewBuilder.buildBackButton;
   const originalContent = AnimalDetailViewBuilder.buildAnimalDetailContent;
   AnimalDetailViewBuilder.buildBackButton = () => {
      const button = document.createElement('button');
      button.className = 'back';
      return button;
   };
   AnimalDetailViewBuilder.buildAnimalDetailContent = () => {
      const content = document.createElement('div');
      content.className = 'detail';
      return content;
   };

   try {
      const view = AnimalDetailView.createAnimalDetailView({ listEl });
      view.render(null, { exhibitName: 'Savanna', onBack: () => {} });
      assert.equal(listEl.children.length, 0);

      view.render({ species: 'Lion' }, { exhibitName: 'Savanna', onBack: () => {} });
      assert.equal(listEl.children.length, 2);
      assert.equal(listEl.scrollTop, 0);
      assert.equal(listEl.children[0].className, 'back');
      assert.equal(listEl.children[1].className, 'detail');
   } finally {
      AnimalDetailViewBuilder.buildBackButton = originalBack;
      AnimalDetailViewBuilder.buildAnimalDetailContent = originalContent;
   }
});
