import assert from 'node:assert/strict';
import { test } from 'node:test';

import { SpeciesFragment } from '../../../scripts/overlays/speciesFragment.js';
import { AnimalsClient } from '../../../scripts/api/animalsClient.js';
import { SpeciesOverlayBuilder } from '../../../scripts/overlays/speciesOverlayBuilder.js';
import { Strings } from '../../../scripts/strings.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';
import { createFetchMock } from '../helpers/fetchMock.mjs';

function _installSpeciesOverlayDom() {
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

function _animalPayload({ species, exhibit, identification }) {
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

installDomTestHooks({
   before: () => {
      SpeciesFragment.speciesOverlayController = null;
      _installSpeciesOverlayDom();
   },
   after: () => {
      SpeciesFragment.speciesOverlayController = null;
      delete globalThis.fetch;
   },
});

test('Test_OpenAnimalSpeciesOverlay_TestOpenAnimalSpeciesOverlayIgnoresAnimalsWithoutASpeciesName_ExpectOk', () => {
   const overlay = document.getElementById('speciesOverlay');
   const content = overlay?.querySelector('.species-overlay-content');

   SpeciesFragment.openAnimalSpeciesOverlay({ species: '   ' });

   assert.equal(overlay?.classList.contains('hidden'), true);
   assert.equal(content?.children.length, Position.FIRST);
});

test('Test_InitSpeciesOverlay_TestInitSpeciesOverlayOpensContentClosesFromBackdropClickAnd_ExpectOk', () => {
   const overlay = document.getElementById('speciesOverlay');
   const content = overlay?.querySelector('.species-overlay-content');
   const first = SpeciesFragment.initSpeciesOverlay();

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
   assert.equal(SpeciesFragment.initSpeciesOverlay(), first);
});

test('Test_OpenAnimalSpeciesOverlay_TestSingleLinked_ExpectNoNav', () => {
   const content = document.getElementById('speciesOverlay')
      ?.querySelector('.species-overlay-content');
   const africanLion = { species: 'African Lion', exhibit: 'Africa Savanna' };

   SpeciesFragment.openAnimalSpeciesOverlay(africanLion, {
      linkedAnimals: [africanLion],
   });

   assert.equal(content?.querySelector('.species-overlay-nav'), null);
});


test('Test_OpenAnimalSpeciesOverlay_TestMultipleLinked_ExpectNav', () => {
   const content = document.getElementById('speciesOverlay')
      ?.querySelector('.species-overlay-content');
   const tamarin = { species: 'Golden Lion Tamarin', exhibit: 'Americas Pavilion' };
   const sloth = { species: 'Two-Toed Sloth', exhibit: 'Americas Pavilion' };
   const saki = { species: 'White-Faced Saki', exhibit: 'Americas Pavilion' };
   const linkedAnimals = [tamarin, sloth, saki];

   SpeciesFragment.openAnimalSpeciesOverlay(tamarin, { linkedAnimals });

   assert.ok(content?.querySelector('.species-overlay-nav'));
   assert.equal(
      content?.querySelector('.species-overlay-nav-position')?.textContent,
      Strings.common.animalPosition(1, linkedAnimals.length)
   );
   assert.ok(content?.querySelector('.species-overlay-nav-prev'));
   assert.ok(content?.querySelector('.species-overlay-nav-next'));
});

test('Test_Species_TestSpeciesOverlayNextArrowFetchesAndSwapsTo_ExpectOk', async () => {
   const content = document.getElementById('speciesOverlay')
      ?.querySelector('.species-overlay-content');
   const requests = [];
   const tamarin = { species: 'Golden Lion Tamarin', exhibit: 'Americas Pavilion' };
   const sloth = { species: 'Two-Toed Sloth', exhibit: 'Americas Pavilion' };
   const saki = { species: 'White-Faced Saki', exhibit: 'Americas Pavilion' };
   const linkedAnimals = [tamarin, sloth, saki];

   globalThis.fetch = createFetchMock({
      '/get-animal-information': (_url, options) => {
         const body = JSON.parse(options.body);
         requests.push(body);

         if (body.species === sloth.species) {
            return _animalPayload({
               species: sloth.species,
               exhibit: sloth.exhibit,
               identification: 'Slow arboreal mammal',
            });
         }

         return _animalPayload({
            species: body.species,
            exhibit: body.exhibit,
            identification: 'Fallback',
         });
      },
   });

   SpeciesFragment.openAnimalSpeciesOverlay(
      {
         ...tamarin,
         identification: 'Bright orange primate',
      },
      { linkedAnimals }
   );
   const nextButton = content?.querySelector('.species-overlay-nav-next');
   nextButton.click();
   await new Promise((resolve) => setTimeout(resolve, 0));

   assert.deepEqual(requests, [sloth]);
   assert.equal(content?.querySelector('.animal-species-name')?.textContent, sloth.species);
   assert.equal(
      content?.querySelector('.species-overlay-nav-position')?.textContent,
      Strings.common.animalPosition(2, linkedAnimals.length)
   );
});

test('Test_InitSpeciesOverlay_TestCloseMissingRenderNavigateGuards_ExpectHandled', async () => {
   const overlay = document.getElementById('speciesOverlay');
   const closeButton = overlay?.querySelector('.species-close');
   const controller = SpeciesFragment.initSpeciesOverlay();

   controller.openFromAnimal({
      species: 'African Lion',
      exhibit: 'Africa Savanna',
      identification: 'Large cat',
   });
   assert.equal(overlay?.classList.contains('hidden'), false);

   closeButton?.listeners.click?.({ stopPropagation() {} });
   assert.equal(overlay?.classList.contains('hidden'), true);

   controller.openFromAnimal(null);
   assert.equal(overlay?.classList.contains('hidden'), true);

   const originalResolve = SpeciesOverlayBuilder.resolveOverlayElements;
   SpeciesOverlayBuilder.resolveOverlayElements = () => ({
      overlay: null,
      content: null,
      closeButton: null,
   });
   try {
      controller.openFromAnimal({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      });
   } finally {
      SpeciesOverlayBuilder.resolveOverlayElements = originalResolve;
   }

   const originalHeader = SpeciesOverlayBuilder.createOverlayHeader;
   SpeciesOverlayBuilder.createOverlayHeader = (options) => {
      const header = originalHeader(options);
      if (options.linkedAnimals.length < 2) {
         void options.onNavigate(1);
      }
      return header;
   };
   try {
      controller.openFromAnimal({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      });
   } finally {
      SpeciesOverlayBuilder.createOverlayHeader = originalHeader;
   }

   const originalGet = AnimalsClient.getAnimalInformation;
   let resolveSlow;
   let fetchCount = 0;
   AnimalsClient.getAnimalInformation = async () => {
      fetchCount += 1;
      await new Promise((resolve) => {
         resolveSlow = resolve;
      });
      return fetchCount === 1
         ? null
         : {
            species: 'Two-Toed Sloth',
            exhibit: 'Americas Pavilion',
         };
   };

   try {
      controller.openFromAnimal(
         {
            species: 'Golden Lion Tamarin',
            exhibit: 'Americas Pavilion',
         },
         {
            linkedAnimals: [
               { species: 'Golden Lion Tamarin', exhibit: 'Americas Pavilion' },
               { species: 'Two-Toed Sloth', exhibit: 'Americas Pavilion' },
            ],
         }
      );

      const nextButton = document.getElementById('speciesOverlay')
         ?.querySelector('.species-overlay-nav-next');
      nextButton.click();
      nextButton.click();
      resolveSlow();
      await new Promise((resolve) => setTimeout(resolve, 0));

      let resolveStale;
      AnimalsClient.getAnimalInformation = async () => {
         await new Promise((resolve) => {
            resolveStale = resolve;
         });
         return {
            species: 'Stale Animal',
            exhibit: 'Americas Pavilion',
         };
      };
      nextButton.click();
      controller.openFromAnimal({
         species: 'Golden Lion Tamarin',
         exhibit: 'Americas Pavilion',
      });
      resolveStale();
      await new Promise((resolve) => setTimeout(resolve, 0));
   } finally {
      AnimalsClient.getAnimalInformation = originalGet;
   }
});
