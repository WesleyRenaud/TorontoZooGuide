import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelector } from '../../../../scripts/itinerary/selectors/animalSelector.js';
import { AnimalSelectorModel } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AnimalSelectorRenderer } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorRenderer.js';
import { AnimalSelectorControllerHelper } from '../../../../scripts/itinerary/selectors/animalSelectorControllerHelper.js';
import { RegionStorageStore } from '../../../../scripts/itinerary/selectors/regionSelector/regionStorageStore.js';
import { SelectorControllerFactory } from '../../../../scripts/itinerary/selectors/selectorControllerFactory.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
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
   const controllerResult = { ok: true };
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return controllerResult;
   };
   AnimalSelectorModel.getAnimalId = (row) => row.id;
   RegionStorageStore.restoreRemovedAnimalKey = () => {};

   try {
      const controller = AnimalSelector.createItineraryAnimalSelectorController({
         mountEl: document.createElement('div'),
      });

      assert.deepEqual(controller, controllerResult);
      assert.equal(captured.storageKey, AnimalSelector.STORAGE_KEY);
      assert.equal(captured.migrateSelected, AnimalSelectorModel.migrateStoredAnimals);
      assert.equal(captured.renderRowLeft, AnimalSelectorRenderer.renderAnimalSelectorRowLeft);
      const animals = [1];
      assert.equal(captured.extractRows({ animals }).at(Position.FIRST), animals.at(Position.FIRST));
      const query = 'lion';
      assert.deepEqual(
         captured.buildSearchPayload(query),
         AnimalSelectorControllerHelper.buildAnimalSearchPayload(query, false)
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


test('Test_OnBeforeToggleAdd_TestNoConfirm_ExpectRestoreAndProceed', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalShouldConfirm = AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal;
   const originalRestore = RegionStorageStore.restoreRemovedAnimalKey;
   const originalGetId = AnimalSelectorModel.getAnimalId;
   let captured;
   const proceeds = [];
   const restores = [];
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   AnimalSelectorModel.getAnimalId = (row) => row.id;
   RegionStorageStore.restoreRemovedAnimalKey = (id) => restores.push(id);
   AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal = () => false;
   const rowId = 'a1';

   try {
      AnimalSelector.createItineraryAnimalSelectorController({
         mountEl: document.createElement('div'),
      });
      captured.onBeforeToggleAdd({
         row: { id: rowId },
         isSelected: false,
         proceed: () => proceeds.push('add'),
      });

      assert.deepEqual(restores, [rowId]);
      assert.deepEqual(proceeds, ['add']);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal = originalShouldConfirm;
      RegionStorageStore.restoreRemovedAnimalKey = originalRestore;
      AnimalSelectorModel.getAnimalId = originalGetId;
   }
});


test('Test_OnBeforeToggleAdd_TestOffDisplay_ExpectPrompt', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalShouldConfirm = AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal;
   const originalPrompt = AnimalSelectorControllerHelper.promptForOffDisplayAnimalSelection;
   const originalRestore = RegionStorageStore.restoreRemovedAnimalKey;
   const originalGetId = AnimalSelectorModel.getAnimalId;
   let captured;
   const proceeds = [];
   const prompts = [];
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   AnimalSelectorModel.getAnimalId = (row) => row.id;
   RegionStorageStore.restoreRemovedAnimalKey = () => {};
   AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal = () => true;
   const rowId = 'a2';
   AnimalSelectorControllerHelper.promptForOffDisplayAnimalSelection = (row, complete) => {
      prompts.push(row.id);
      complete();
   };

   try {
      AnimalSelector.createItineraryAnimalSelectorController({
         mountEl: document.createElement('div'),
      });
      captured.onBeforeToggleAdd({
         row: { id: rowId },
         isSelected: true,
         proceed: () => proceeds.push('confirm'),
      });

      assert.deepEqual(prompts, [rowId]);
      assert.ok(proceeds.includes('confirm'));
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal = originalShouldConfirm;
      AnimalSelectorControllerHelper.promptForOffDisplayAnimalSelection = originalPrompt;
      RegionStorageStore.restoreRemovedAnimalKey = originalRestore;
      AnimalSelectorModel.getAnimalId = originalGetId;
   }
});


test('Test_RenderExtraControls_TestIncludeOffDisplay_ExpectSearchPayload', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalRender = AnimalSelectorControllerHelper.renderOffDisplayAnimalControls;
   const originalGetId = AnimalSelectorModel.getAnimalId;
   let captured;
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   AnimalSelectorModel.getAnimalId = (row) => row.id;
   AnimalSelectorControllerHelper.renderOffDisplayAnimalControls = ({ onChange }) => {
      onChange(true);
   };
   const query = 'lion';

   try {
      AnimalSelector.createItineraryAnimalSelectorController({
         mountEl: document.createElement('div'),
      });
      captured.renderExtraControls({
         bodyEl: document.createElement('div'),
         rerunSearch: () => {},
      });

      assert.deepEqual(
         captured.buildSearchPayload(query),
         AnimalSelectorControllerHelper.buildAnimalSearchPayload(query, true)
      );
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AnimalSelectorControllerHelper.renderOffDisplayAnimalControls = originalRender;
      AnimalSelectorModel.getAnimalId = originalGetId;
   }
});
