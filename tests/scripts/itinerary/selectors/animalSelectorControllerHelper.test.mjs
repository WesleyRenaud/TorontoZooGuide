import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelectorControllerHelper } from '../../../../scripts/itinerary/selectors/animalSelectorControllerHelper.js';
import { AnimalSelectorModel } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AnimalSelectorRenderer } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorRenderer.js';
import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_GetAnimalTitle_TestRow_ExpectModelTitle', () => {
   const original = AnimalSelectorModel.getAnimalTitleLine;
   AnimalSelectorModel.getAnimalTitleLine = () => 'African Lion';

   try {
      assert.equal(AnimalSelectorControllerHelper.getAnimalTitle({ species: 'African Lion' }), 'African Lion');
   } finally {
      AnimalSelectorModel.getAnimalTitleLine = original;
   }
});

test('Test_BuildAnimalSearchPayload_TestFlags_ExpectPayload', () => {
   assert.deepEqual(AnimalSelectorControllerHelper.buildAnimalSearchPayload('lion', true), {
      query: 'lion',
      includeAnimals: true,
      includeOffDisplayAnimals: true,
      forItinerary: true,
   });
});

test('Test_ShouldConfirmOffDisplayAnimal_TestCases_ExpectBoolean', () => {
   const original = AnimalSelectorModel.isLikelyOffDisplayAnimal;
   AnimalSelectorModel.isLikelyOffDisplayAnimal = () => true;

   try {
      assert.equal(AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal({
         row: {},
         isSelected: true,
         includeOffDisplayAnimals: true,
      }), false);
      assert.equal(AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal({
         row: {},
         isSelected: false,
         includeOffDisplayAnimals: false,
      }), false);
      assert.equal(AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal({
         row: {},
         isSelected: false,
         includeOffDisplayAnimals: true,
      }), true);
   } finally {
      AnimalSelectorModel.isLikelyOffDisplayAnimal = original;
   }
});

test('Test_PromptForOffDisplayAnimalSelection_TestRow_ExpectConfirmPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMessage = AnimalSelectorModel.buildOffDisplayWarningMessage;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   AnimalSelectorModel.buildOffDisplayWarningMessage = () => 'May be off display';

   try {
      const proceed = () => {};
      AnimalSelectorControllerHelper.promptForOffDisplayAnimalSelection({ species: 'Lion' }, proceed);
      assert.equal(calls.length, 1);
      assert.equal(calls[0].title, Strings.itinerary.confirmation.animalMayBeOffDisplay);
      assert.equal(calls[0].message, 'May be off display');
      assert.equal(calls[0].confirmText, Strings.itinerary.actions.add);
      assert.equal(calls[0].cancelText, Strings.itinerary.actions.cancel);
      assert.equal(calls[0].onConfirm, proceed);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      AnimalSelectorModel.buildOffDisplayWarningMessage = originalMessage;
   }
});

test('Test_RenderOffDisplayAnimalControls_TestArgs_ExpectRenderer', () => {
   const calls = [];
   const original = AnimalSelectorRenderer.renderIncludeOffDisplayToggle;
   AnimalSelectorRenderer.renderIncludeOffDisplayToggle = (args) => { calls.push(args); };

   try {
      const bodyEl = { id: 'body' };
      const rerunSearch = () => {};
      const onChange = () => {};
      AnimalSelectorControllerHelper.renderOffDisplayAnimalControls({ bodyEl, rerunSearch, onChange });
      assert.deepEqual(calls, [{ bodyEl, rerunSearch, onChange }]);
   } finally {
      AnimalSelectorRenderer.renderIncludeOffDisplayToggle = original;
   }
});
