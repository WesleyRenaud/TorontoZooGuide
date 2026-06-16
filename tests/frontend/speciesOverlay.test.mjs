import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   initSpeciesOverlay,
   openAnimalSpeciesOverlay,
} from '../../scripts/overlays/speciesOverlay.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

function installSpeciesOverlayDom() {
   const overlay = createDomNode('div', 'species-overlay hidden');
   overlay.id = 'speciesOverlay';
   overlay.classList.add('hidden');

   const content = createDomNode('div', 'species-overlay-content');
   overlay.appendChild(content);

   const previousGetElementById = document.getElementById.bind(document);

   document.getElementById = (id) => {
      if (id === 'speciesOverlay') {
         return overlay;
      }

      return previousGetElementById(id);
   };

   return { overlay, content };
}

test.describe('species overlay', () => {
   installDomTestHooks({
      before: () => {
         installSpeciesOverlayDom();
      },
   });

   test('openAnimalSpeciesOverlay ignores animals without a species name', () => {
      const overlay = document.getElementById('speciesOverlay');
      const content = overlay?.querySelector('.species-overlay-content');

      openAnimalSpeciesOverlay({ species: '   ' });

      assert.equal(overlay?.classList.contains('hidden'), true);
      assert.equal(content?.children.length, 0);
   });

   test('initSpeciesOverlay opens content, closes from backdrop click, and reuses controller', () => {
      const overlay = document.getElementById('speciesOverlay');
      const content = overlay?.querySelector('.species-overlay-content');
      const first = initSpeciesOverlay();

      first.openFromAnimal({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
         identification: 'Large cat with a mane',
      });

      assert.equal(overlay?.classList.contains('hidden'), false);
      assert.ok(content?.querySelector('.species-overlay-header'));
      assert.ok(content?.querySelector('.animal-species-name'));

      overlay?.listeners.click?.({ target: overlay });
      assert.equal(overlay?.classList.contains('hidden'), true);
      assert.equal(initSpeciesOverlay(), first);
   });
});
