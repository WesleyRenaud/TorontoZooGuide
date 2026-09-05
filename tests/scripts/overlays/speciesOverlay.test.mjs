import assert from 'node:assert/strict';
import { test } from 'node:test';

import { SpeciesOverlay } from '../../../scripts/overlays/speciesOverlay.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';
import { createFetchMock } from '../helpers/fetchMock.mjs';

function installSpeciesOverlayDom() {
   const overlay = createDomNode('div', 'species-overlay hidden');
   overlay.id = 'speciesOverlay';
   overlay.classList.add('hidden');

   const card = createDomNode('div', 'species-overlay-card');
   const closeButton = createDomNode('button', 'species-close');
   const content = createDomNode('div', 'species-overlay-content');

   card.appendChild(closeButton);
   card.appendChild(content);
   overlay.appendChild(card);

   const previousGetElementById = document.getElementById.bind(document);

   document.getElementById = (id) => {
      if (id === 'speciesOverlay') {
         return overlay;
      }

      return previousGetElementById(id);
   };

   return { overlay, content, closeButton };
}

function animalPayload({ species, exhibit, identification }) {
   return {
      information: [
         {
            species,
            exhibit,
            identification,
         },
      ],
   };
}

test.describe('species overlay', () => {
   installDomTestHooks({
      before: () => {
         installSpeciesOverlayDom();
      },
      after: () => {
         delete globalThis.fetch;
      },
   });

   test('Test_OpenAnimalSpeciesOverlay_TestOpenAnimalSpeciesOverlayIgnoresAnimalsWithoutASpeciesName_ExpectOk', () => {
      const overlay = document.getElementById('speciesOverlay');
      const content = overlay?.querySelector('.species-overlay-content');

      SpeciesOverlay.openAnimalSpeciesOverlay({ species: '   ' });

      assert.equal(overlay?.classList.contains('hidden'), true);
      assert.equal(content?.children.length, 0);
   });

   test('Test_InitSpeciesOverlay_TestInitSpeciesOverlayOpensContentClosesFromBackdropClickAnd_ExpectOk', () => {
      const overlay = document.getElementById('speciesOverlay');
      const content = overlay?.querySelector('.species-overlay-content');
      const first = SpeciesOverlay.initSpeciesOverlay();

      first.openFromAnimal({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
         identification: 'Large cat with a mane',
      });

      assert.equal(overlay?.classList.contains('hidden'), false);
      assert.ok(content?.querySelector('.species-overlay-header'));
      assert.ok(content?.querySelector('.animal-species-name'));
      assert.equal(content?.querySelector('.species-overlay-nav'), null);
      assert.equal(
         overlay?.querySelector('.species-close')?.textContent,
         '×'
      );

      overlay?.listeners.click?.({ target: overlay });
      assert.equal(overlay?.classList.contains('hidden'), true);
      assert.equal(SpeciesOverlay.initSpeciesOverlay(), first);
   });

   test('Test_OpenAnimalSpeciesOverlay_TestOpenAnimalSpeciesOverlayShowsLinkedAnimalNavOnlyForMultiple_ExpectOk', () => {
      const content = document.getElementById('speciesOverlay')
         ?.querySelector('.species-overlay-content');

      SpeciesOverlay.openAnimalSpeciesOverlay(
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
         },
         {
            linkedAnimals: [
               { species: 'African Lion', exhibit: 'Africa Savanna' },
            ],
         }
      );

      assert.equal(content?.querySelector('.species-overlay-nav'), null);

      SpeciesOverlay.openAnimalSpeciesOverlay(
         {
            species: 'Golden Lion Tamarin',
            exhibit: 'Americas Pavilion',
         },
         {
            linkedAnimals: [
               { species: 'Golden Lion Tamarin', exhibit: 'Americas Pavilion' },
               { species: 'Two-Toed Sloth', exhibit: 'Americas Pavilion' },
               { species: 'White-Faced Saki', exhibit: 'Americas Pavilion' },
            ],
         }
      );

      assert.ok(content?.querySelector('.species-overlay-nav'));
      assert.equal(
         content?.querySelector('.species-overlay-nav-position')?.textContent,
         '1 of 3'
      );
      assert.ok(content?.querySelector('.species-overlay-nav-prev'));
      assert.ok(content?.querySelector('.species-overlay-nav-next'));
   });

   test('Test_Species_TestSpeciesOverlayNextArrowFetchesAndSwapsTo_ExpectOk', async () => {
      const content = document.getElementById('speciesOverlay')
         ?.querySelector('.species-overlay-content');
      const requests = [];

      globalThis.fetch = createFetchMock({
         '/get-animal-information': (_url, options) => {
            const body = JSON.parse(options.body);
            requests.push(body);

            if (body.species === 'Two-Toed Sloth') {
               return animalPayload({
                  species: 'Two-Toed Sloth',
                  exhibit: 'Americas Pavilion',
                  identification: 'Slow arboreal mammal',
               });
            }

            return animalPayload({
               species: body.species,
               exhibit: body.exhibit,
               identification: 'Fallback',
            });
         },
      });

      SpeciesOverlay.openAnimalSpeciesOverlay(
         {
            species: 'Golden Lion Tamarin',
            exhibit: 'Americas Pavilion',
            identification: 'Bright orange primate',
         },
         {
            linkedAnimals: [
               { species: 'Golden Lion Tamarin', exhibit: 'Americas Pavilion' },
               { species: 'Two-Toed Sloth', exhibit: 'Americas Pavilion' },
               { species: 'White-Faced Saki', exhibit: 'Americas Pavilion' },
            ],
         }
      );

      assert.equal(
         content?.querySelector('.animal-species-name')?.textContent,
         'Golden Lion Tamarin'
      );

      const nextButton = content?.querySelector('.species-overlay-nav-next');
      assert.ok(nextButton);
      nextButton.click();
      await new Promise((resolve) => setTimeout(resolve, 0));

      assert.deepEqual(requests, [
         { species: 'Two-Toed Sloth', exhibit: 'Americas Pavilion' },
      ]);
      assert.equal(
         content?.querySelector('.animal-species-name')?.textContent,
         'Two-Toed Sloth'
      );
      assert.equal(
         content?.querySelector('.species-overlay-nav-position')?.textContent,
         '2 of 3'
      );
   });
});
