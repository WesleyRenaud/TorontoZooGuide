import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelectorControllerHelper } from '../../../../scripts/itinerary/selectors/animalSelectorControllerHelper.js';
import { AnimalSelectorModel } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AnimalSelectorRenderer } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorRenderer.js';
import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_GetAnimalTitle_TestRow_ExpectModelTitle', () => {
   const original = AnimalSelectorModel.getAnimalTitleLine;
   const title = 'African Lion';
   AnimalSelectorModel.getAnimalTitleLine = () => title;

   try {
      const animalTitle = AnimalSelectorControllerHelper.getAnimalTitle({ species: title });

      assert.equal(animalTitle, title);
   } finally {
      AnimalSelectorModel.getAnimalTitleLine = original;
   }
});


test('Test_BuildAnimalSearchPayload_TestFlags_ExpectPayload', () => {
   const query = 'lion';
   const includeOffDisplayAnimals = true;

   const payload = AnimalSelectorControllerHelper.buildAnimalSearchPayload(
      query,
      includeOffDisplayAnimals
   );

   assert.equal(payload.query, query);
   assert.equal(payload.includeAnimals, true);
   assert.equal(payload.includeOffDisplayAnimals, includeOffDisplayAnimals);
   assert.equal(payload.forItinerary, true);
});


test('Test_ShouldConfirmOffDisplayAnimal_TestAlreadySelected_ExpectFalse', () => {
   const original = AnimalSelectorModel.isLikelyOffDisplayAnimal;
   AnimalSelectorModel.isLikelyOffDisplayAnimal = () => true;

   try {
      const shouldConfirm = AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal({
         row: {},
         isSelected: true,
         includeOffDisplayAnimals: true,
      });

      assert.equal(shouldConfirm, false);
   } finally {
      AnimalSelectorModel.isLikelyOffDisplayAnimal = original;
   }
});


test('Test_ShouldConfirmOffDisplayAnimal_TestHiddenOffDisplay_ExpectFalse', () => {
   const original = AnimalSelectorModel.isLikelyOffDisplayAnimal;
   AnimalSelectorModel.isLikelyOffDisplayAnimal = () => true;

   try {
      const shouldConfirm = AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal({
         row: {},
         isSelected: false,
         includeOffDisplayAnimals: false,
      });

      assert.equal(shouldConfirm, false);
   } finally {
      AnimalSelectorModel.isLikelyOffDisplayAnimal = original;
   }
});


test('Test_ShouldConfirmOffDisplayAnimal_TestAddingOffDisplay_ExpectTrue', () => {
   const original = AnimalSelectorModel.isLikelyOffDisplayAnimal;
   AnimalSelectorModel.isLikelyOffDisplayAnimal = () => true;

   try {
      const shouldConfirm = AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal({
         row: {},
         isSelected: false,
         includeOffDisplayAnimals: true,
      });

      assert.equal(shouldConfirm, true);
   } finally {
      AnimalSelectorModel.isLikelyOffDisplayAnimal = original;
   }
});


test('Test_PromptForOffDisplayAnimalSelection_TestRow_ExpectConfirmPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMessage = AnimalSelectorModel.buildOffDisplayWarningMessage;
   const message = 'May be off display';
   const proceed = () => {};
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   AnimalSelectorModel.buildOffDisplayWarningMessage = () => message;

   try {
      AnimalSelectorControllerHelper.promptForOffDisplayAnimalSelection({ species: 'Lion' }, proceed);

      assert.equal(calls.length, 1);
      assert.equal(calls.at(Position.FIRST).title, Strings.itinerary.confirmation.animalMayBeOffDisplay);
      assert.equal(calls.at(Position.FIRST).message, message);
      assert.equal(calls.at(Position.FIRST).confirmText, Strings.itinerary.actions.add);
      assert.equal(calls.at(Position.FIRST).cancelText, Strings.itinerary.actions.cancel);
      assert.equal(calls.at(Position.FIRST).onConfirm, proceed);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      AnimalSelectorModel.buildOffDisplayWarningMessage = originalMessage;
   }
});


test('Test_RenderOffDisplayAnimalControls_TestArgs_ExpectRenderer', () => {
   const calls = [];
   const original = AnimalSelectorRenderer.renderIncludeOffDisplayToggle;
   AnimalSelectorRenderer.renderIncludeOffDisplayToggle = (args) => { calls.push(args); };
   const bodyEl = { id: 'body' };
   const rerunSearch = () => {};
   const onChange = () => {};

   try {
      AnimalSelectorControllerHelper.renderOffDisplayAnimalControls({ bodyEl, rerunSearch, onChange });

      assert.deepEqual(calls.at(Position.FIRST), { bodyEl, rerunSearch, onChange });
   } finally {
      AnimalSelectorRenderer.renderIncludeOffDisplayToggle = original;
   }
});
