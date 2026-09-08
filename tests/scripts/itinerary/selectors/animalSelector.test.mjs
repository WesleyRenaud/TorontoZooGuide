import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelector } from '../../../../scripts/itinerary/selectors/animalSelector.js';
import { AnimalSelectorModel } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AnimalSelectorRenderer } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorRenderer.js';
import { AnimalSelectorControllerHelper } from '../../../../scripts/itinerary/selectors/animalSelectorControllerHelper.js';
import { RegionStorageStore } from '../../../../scripts/itinerary/selectors/regionSelector/regionStorageStore.js';
import { SelectorControllerFactory } from '../../../../scripts/itinerary/selectors/selectorControllerFactory.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateItineraryAnimalSelectorController_TestWiring_ExpectFactoryConfig', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalShouldConfirm = AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal;
   const originalPrompt = AnimalSelectorControllerHelper.promptForOffDisplayAnimalSelection;
   const originalRender = AnimalSelectorControllerHelper.renderOffDisplayAnimalControls;
   const originalRestore = RegionStorageStore.restoreRemovedAnimalKey;
   const originalGetId = AnimalSelectorModel.getAnimalId;
   let captured;
   const proceeds = [];
   const restores = [];
   const prompts = [];

   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   AnimalSelectorModel.getAnimalId = (row) => row.id;
   RegionStorageStore.restoreRemovedAnimalKey = (id) => restores.push(id);

   try {
      const controller = AnimalSelector.createItineraryAnimalSelectorController({
         mountEl: document.createElement('div'),
      });

      assert.deepEqual(controller, { ok: true });
      assert.equal(captured.storageKey, AnimalSelector.STORAGE_KEY);
      assert.equal(captured.migrateSelected, AnimalSelectorModel.migrateStoredAnimals);
      assert.equal(captured.extractRows({ animals: [1] })[0], 1);
      assert.equal(captured.renderRowLeft, AnimalSelectorRenderer.renderAnimalSelectorRowLeft);
      assert.deepEqual(
         captured.buildSearchPayload('lion'),
         AnimalSelectorControllerHelper.buildAnimalSearchPayload('lion', false)
      );

      AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal = () => false;
      captured.onBeforeToggleAdd({
         row: { id: 'a1' },
         isSelected: false,
         proceed: () => proceeds.push('add'),
      });
      assert.deepEqual(restores, ['a1']);
      assert.deepEqual(proceeds, ['add']);

      AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal = () => true;
      AnimalSelectorControllerHelper.promptForOffDisplayAnimalSelection = (row, complete) => {
         prompts.push(row.id);
         complete();
      };
      captured.onBeforeToggleAdd({
         row: { id: 'a2' },
         isSelected: true,
         proceed: () => proceeds.push('confirm'),
      });
      assert.deepEqual(prompts, ['a2']);
      assert.ok(proceeds.includes('confirm'));

      AnimalSelectorControllerHelper.renderOffDisplayAnimalControls = ({ onChange }) => {
         onChange(true);
      };
      captured.renderExtraControls({
         bodyEl: document.createElement('div'),
         rerunSearch: () => {},
      });
      assert.deepEqual(
         captured.buildSearchPayload('lion'),
         AnimalSelectorControllerHelper.buildAnimalSearchPayload('lion', true)
      );
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal = originalShouldConfirm;
      AnimalSelectorControllerHelper.promptForOffDisplayAnimalSelection = originalPrompt;
      AnimalSelectorControllerHelper.renderOffDisplayAnimalControls = originalRender;
      RegionStorageStore.restoreRemovedAnimalKey = originalRestore;
      AnimalSelectorModel.getAnimalId = originalGetId;
   }
});
