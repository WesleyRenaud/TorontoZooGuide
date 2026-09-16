import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleControllersBootstrapHelper } from '../../../../scripts/consoleOperations/bootstrap/consoleControllersBootstrapHelper.js';
import { AnimalSpeciesController } from '../../../../scripts/consoleOperations/animals/controllers/animalSpeciesController.js';
import { SpeciesProvider } from '../../../../scripts/consoleOperations/animals/autocomplete/speciesProvider.js';

test('Test_AnimalSpeciesAutocompleteKeys_TestRegistry_ExpectKnownKeys', () => {
   assert.deepEqual(ConsoleControllersBootstrapHelper.ANIMAL_SPECIES_AUTOCOMPLETE_KEYS, [
      'offDisplay',
      'onDisplay',
      'visibilitySchedule',
      'removeVisibilitySchedule',
      'viewingAlert',
      'removeViewingAlert',
   ]);
   assert.deepEqual(ConsoleControllersBootstrapHelper.ANIMAL_SPECIES_SOURCE_METHOD_BY_KEY, {
      onDisplay: 'createOffDisplayAnimalSpeciesSource',
   });
});

test('Test_ControllerBindings_TestRegistry_ExpectCreateFunctions', () => {
   const bindings = ConsoleControllersBootstrapHelper.CONTROLLER_BINDINGS;

   assert.ok(Array.isArray(bindings));
   assert.ok(bindings.length >= 30);
   assert.ok(bindings.every((binding) => typeof binding.createController === 'function'));
   assert.ok(bindings.every((binding) => typeof binding.getRefs === 'function'));
});

test('Test_ControllerBindings_TestGetExtraOptions_ExpectSpecialControllersMapped', () => {
   const specialControllers = {
      guardiansTalkScheduleLocationFilterController: { id: 'gt-schedule-location' },
      endGuardiansTalkScheduleLocationFilterController: { id: 'gt-end-location' },
      guardiansTalkScheduleTimesFilterController: { id: 'gt-schedule-times' },
      addGuardiansTalkOccurrenceLocationFilterController: { id: 'gt-add-location' },
      cancelGuardiansTalkOccurrenceLocationFilterController: { id: 'gt-cancel-location' },
      cancelGuardiansTalkOccurrenceFilterController: { id: 'gt-cancel-occurrence' },
      wildEncounterScheduleTimesFilterController: { id: 'we-schedule-times' },
      wildEncounterOccurrenceFilterController: { id: 'we-occurrence' },
   };

   const extras = ConsoleControllersBootstrapHelper.CONTROLLER_BINDINGS
      .filter((binding) => typeof binding.getExtraOptions === 'function')
      .map((binding) => binding.getExtraOptions(specialControllers));

   assert.deepEqual(extras, [
      {
         talkLocationFilterController: specialControllers.guardiansTalkScheduleLocationFilterController,
      },
      {
         talkLocationFilterController: specialControllers.endGuardiansTalkScheduleLocationFilterController,
         scheduleTimesFilterController: specialControllers.guardiansTalkScheduleTimesFilterController,
      },
      {
         talkLocationFilterController: specialControllers.addGuardiansTalkOccurrenceLocationFilterController,
      },
      {
         talkLocationFilterController: specialControllers.cancelGuardiansTalkOccurrenceLocationFilterController,
         occurrenceFilterController: specialControllers.cancelGuardiansTalkOccurrenceFilterController,
      },
      {
         scheduleTimesFilterController: specialControllers.wildEncounterScheduleTimesFilterController,
      },
      {
         occurrenceFilterController: specialControllers.wildEncounterOccurrenceFilterController,
      },
   ]);
});

test('Test_CreateAnimalSpeciesSourceForKey_TestOnDisplayAndDefault_ExpectMatchingSources', () => {
   const originalDefault = SpeciesProvider.createAnimalSpeciesSource;
   const originalOffDisplay = SpeciesProvider.createOffDisplayAnimalSpeciesSource;
   const defaultSource = { kind: 'default' };
   const offDisplaySource = { kind: 'off-display' };

   SpeciesProvider.createAnimalSpeciesSource = () => defaultSource;
   SpeciesProvider.createOffDisplayAnimalSpeciesSource = () => offDisplaySource;

   try {
      assert.equal(
         ConsoleControllersBootstrapHelper.createAnimalSpeciesSourceForKey('onDisplay'),
         offDisplaySource
      );
      assert.equal(
         ConsoleControllersBootstrapHelper.createAnimalSpeciesSourceForKey('offDisplay'),
         defaultSource
      );
   } finally {
      SpeciesProvider.createAnimalSpeciesSource = originalDefault;
      SpeciesProvider.createOffDisplayAnimalSpeciesSource = originalOffDisplay;
   }
});

test('Test_InitAnimalSpeciesAutocompletes_TestAnimalsRefs_ExpectControllersCreated', () => {
   const originalCreate = AnimalSpeciesController.createAnimalSpeciesAutocompleteController;
   const originalDefault = SpeciesProvider.createAnimalSpeciesSource;
   const originalOffDisplay = SpeciesProvider.createOffDisplayAnimalSpeciesSource;
   const calls = [];
   const defaultSource = { kind: 'default' };
   const offDisplaySource = { kind: 'off-display' };

   AnimalSpeciesController.createAnimalSpeciesAutocompleteController = (options) => {
      calls.push(options);
      return { created: true };
   };
   SpeciesProvider.createAnimalSpeciesSource = () => defaultSource;
   SpeciesProvider.createOffDisplayAnimalSpeciesSource = () => offDisplaySource;

   try {
      const animals = Object.fromEntries(
         ConsoleControllersBootstrapHelper.ANIMAL_SPECIES_AUTOCOMPLETE_KEYS.map((key) => [
            key,
            {
               speciesEl: { id: `${key}-species` },
               speciesResultsEl: { id: `${key}-results` },
               exhibitEl: { id: `${key}-exhibit` },
            },
         ])
      );

      ConsoleControllersBootstrapHelper.initAnimalSpeciesAutocompletes(animals);

      assert.equal(calls.length, 6);
      assert.deepEqual(calls[0], {
         inputEl: animals.offDisplay.speciesEl,
         resultsEl: animals.offDisplay.speciesResultsEl,
         exhibitEl: animals.offDisplay.exhibitEl,
         speciesSource: defaultSource,
      });
      assert.equal(calls[1].speciesSource, offDisplaySource);
   } finally {
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController = originalCreate;
      SpeciesProvider.createAnimalSpeciesSource = originalDefault;
      SpeciesProvider.createOffDisplayAnimalSpeciesSource = originalOffDisplay;
   }
});

test('Test_CreateControllerOptions_TestExtraOptions_ExpectMerged', () => {
   const activatePanel = () => {};
   const options = ConsoleControllersBootstrapHelper.createControllerOptions({
      refs: { panelEl: { id: 'panel' }, statusEl: {} },
      activatePanel,
      getExtraOptions: (specialControllers) => ({
         occurrenceFilterController: specialControllers.filter,
      }),
      specialControllers: { filter: { id: 'filter' } },
   });

   assert.equal(options.panelEl.id, 'panel');
   assert.equal(options.activatePanel, activatePanel);
   assert.deepEqual(options.occurrenceFilterController, { id: 'filter' });
});

test('Test_CreateControllerOptions_TestWithoutExtra_ExpectRefsOnly', () => {
   const options = ConsoleControllersBootstrapHelper.createControllerOptions({
      refs: { panelEl: { id: 'panel' } },
      activatePanel: null,
   });

   assert.deepEqual(options, {
      panelEl: { id: 'panel' },
      activatePanel: null,
   });
});

test('Test_WireControllerBindings_TestStubbedBinding_ExpectCreateCalled', () => {
   const originalBindings = ConsoleControllersBootstrapHelper.CONTROLLER_BINDINGS;
   const calls = [];
   const activatePanel = () => {};
   const specialControllers = { filter: { id: 'filter' } };

   ConsoleControllersBootstrapHelper.CONTROLLER_BINDINGS = [
      {
         createController: (options) => {
            calls.push(options);
         },
         getRefs: (refs) => refs.animals.offDisplay,
         getExtraOptions: ({ filter }) => ({ occurrenceFilterController: filter }),
      },
      {
         createController: (options) => {
            calls.push(['second', options.panelEl]);
         },
         getRefs: (refs) => refs.animals.onDisplay,
      },
   ];

   try {
      ConsoleControllersBootstrapHelper.wireControllerBindings({
         refs: {
            animals: {
               offDisplay: { panelEl: { id: 'off' }, statusEl: {} },
               onDisplay: { panelEl: { id: 'on' }, statusEl: {} },
            },
         },
         activatePanel,
         specialControllers,
      });

      assert.equal(calls.length, 2);
      assert.equal(calls[0].panelEl.id, 'off');
      assert.equal(calls[0].activatePanel, activatePanel);
      assert.deepEqual(calls[0].occurrenceFilterController, { id: 'filter' });
      assert.deepEqual(calls[1], ['second', { id: 'on' }]);
   } finally {
      ConsoleControllersBootstrapHelper.CONTROLLER_BINDINGS = originalBindings;
   }
});