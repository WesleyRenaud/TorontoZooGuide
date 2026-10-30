import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkLocationFilter } from '../../../../../scripts/consoleOperations/guardiansTalks/controllers/guardiansTalkLocationFilter.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateGuardiansTalkLocationFilterController_TestRefreshLocations_ExpectSortedNames', async () => {
   const locationEl = document.createElement('select');
   const talkNameEl = document.createElement('select');
   const originalGet = ConsoleOperationsClient.getGuardiansTalkLocations;
   const originalPopulate = ConsoleDropdownPopulator.populateValueDropdown;
   let captured;

   ConsoleOperationsClient.getGuardiansTalkLocations = async () => ({
      guardians_talk_locations: [
         { location: 'Zoonoonie' },
         'Eurasia',
         { name: 'Americas' },
         { location: '' },
      ],
   });
   ConsoleDropdownPopulator.populateValueDropdown = (el, names, label) => {
      captured = { el, names, label };
   };

   try {
      const controller = GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
         locationEl,
         talkNameEl,
      });

      await controller.refreshLocations();
      assert.equal(captured.el, locationEl);
      assert.equal(captured.label, Strings.placeholders.location);
      assert.deepEqual(captured.names, ['Americas', 'Eurasia', 'Zoonoonie']);
   } finally {
      ConsoleOperationsClient.getGuardiansTalkLocations = originalGet;
      ConsoleDropdownPopulator.populateValueDropdown = originalPopulate;
   }
});


test('Test_CreateGuardiansTalkLocationFilterController_TestRefreshTalks_ExpectPopulateOrClear', async () => {
   const locationEl = document.createElement('select');
   const talkNameEl = document.createElement('select');
   const originalGetField = ControllerHelper.getFieldValue;
   const originalGetTalks = ConsoleOperationsClient.getGuardiansTalkNamesAtLocation;
   const originalPopulateTalks = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;
   const talkCalls = [];

   ControllerHelper.getFieldValue = () => 'Eurasia';
   ConsoleOperationsClient.getGuardiansTalkNamesAtLocation = async ({ location }) => ({
      guardians_talks: [{ name: `${location} Talk` }],
   });
   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = (el, talks) => {
      talkCalls.push({ el, talks });
   };

   try {
      const controller = GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
         locationEl,
         talkNameEl,
      });

      await controller.refresh();
      assert.deepEqual(talkCalls.at(-1), {
         el: talkNameEl,
         talks: [{ name: 'Eurasia Talk' }],
      });

      ControllerHelper.getFieldValue = () => '';
      talkCalls.length = 0;
      await controller.refresh();
      assert.deepEqual(talkCalls, [{ el: talkNameEl, talks: [] }]);

      controller.clear();
      assert.deepEqual(talkCalls.at(-1), { el: talkNameEl, talks: [] });
   } finally {
      ControllerHelper.getFieldValue = originalGetField;
      ConsoleOperationsClient.getGuardiansTalkNamesAtLocation = originalGetTalks;
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulateTalks;
   }
});


test('Test_CreateGuardiansTalkLocationFilterController_TestInjectedLoaders_ExpectUsed', async () => {
   const locationEl = document.createElement('select');
   const talkNameEl = document.createElement('select');
   const originalGetField = ControllerHelper.getFieldValue;
   const originalPopulateLocations = ConsoleDropdownPopulator.populateValueDropdown;
   const originalPopulateTalks = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;
   const locationCalls = [];
   const talkCalls = [];

   ControllerHelper.getFieldValue = () => 'Africa Savanna';
   ConsoleDropdownPopulator.populateValueDropdown = (el, names) => {
      locationCalls.push({ el, names });
   };
   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = (el, talks) => {
      talkCalls.push({ el, talks });
   };

   try {
      const controller = GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
         locationEl,
         talkNameEl,
         loadLocations: async () => ({
            guardians_talk_locations: ['Africa Savanna'],
         }),
         loadTalks: async ({ location }) => ({
            guardians_talks: [`${location} Talk`],
         }),
      });

      await controller.refreshLocations();
      await controller.refresh();

      assert.deepEqual(locationCalls.at(Position.LAST), {
         el: locationEl,
         names: ['Africa Savanna'],
      });
      assert.deepEqual(talkCalls.at(Position.LAST), {
         el: talkNameEl,
         talks: ['Africa Savanna Talk'],
      });
   } finally {
      ControllerHelper.getFieldValue = originalGetField;
      ConsoleDropdownPopulator.populateValueDropdown = originalPopulateLocations;
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulateTalks;
   }
});


test('Test_CreateGuardiansTalkLocationFilterController_TestChangeClearsTalk_ExpectRefresh', async () => {
   const locationEl = document.createElement('select');
   const talkNameEl = document.createElement('input');
   talkNameEl.value = 'Old Talk';
   const originalGetField = ControllerHelper.getFieldValue;
   const originalGetTalks = ConsoleOperationsClient.getGuardiansTalkNamesAtLocation;
   let refreshed = 0;

   ControllerHelper.getFieldValue = () => 'Americas';
   ConsoleOperationsClient.getGuardiansTalkNamesAtLocation = async () => {
      refreshed += 1;
      return { guardians_talks: [] };
   };

   try {
      GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
         locationEl,
         talkNameEl,
      });

      await locationEl.listeners.change();
      assert.equal(talkNameEl.value, '');
      assert.equal(refreshed, 1);
   } finally {
      ControllerHelper.getFieldValue = originalGetField;
      ConsoleOperationsClient.getGuardiansTalkNamesAtLocation = originalGetTalks;
   }
});


test('Test_CreateGuardiansTalkLocationFilterController_TestNonSelectAndErrors_ExpectNoThrow', async () => {
   const originalGetLocations = ConsoleOperationsClient.getGuardiansTalkLocations;
   const originalGetTalks = ConsoleOperationsClient.getGuardiansTalkNamesAtLocation;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalPopulateTalks = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;

   ConsoleOperationsClient.getGuardiansTalkLocations = async () => {
      throw new Error('locations failed');
   };
   ConsoleOperationsClient.getGuardiansTalkNamesAtLocation = async () => {
      throw new Error('talks failed');
   };
   ControllerHelper.getFieldValue = () => 'Eurasia';
   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = () => {};

   try {
      const locationInputEl = document.createElement('input');
      const talkInputEl = document.createElement('input');
      talkInputEl.value = 'Talk';
      const nonSelectController = GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
         locationEl: locationInputEl,
         talkNameEl: talkInputEl,
      });

      await nonSelectController.refreshLocations();
      nonSelectController.clear();
      assert.equal(talkInputEl.value, '');

      const locationEl = document.createElement('select');
      const talkNameEl = document.createElement('select');
      const controller = GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
         locationEl,
         talkNameEl,
      });

      await controller.refreshLocations();
      await controller.refresh();
   } finally {
      ConsoleOperationsClient.getGuardiansTalkLocations = originalGetLocations;
      ConsoleOperationsClient.getGuardiansTalkNamesAtLocation = originalGetTalks;
      ControllerHelper.getFieldValue = originalGetField;
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulateTalks;
   }
});


test('Test_CreateGuardiansTalkLocationFilterController_TestDuplicateTalkNames_ExpectEnclosureChoices', async () => {
   const locationEl = document.createElement('select');
   const talkNameEl = document.createElement('select');
   const enclosureEl = document.createElement('select');
   const enclosureFieldEl = document.createElement('div');

   enclosureFieldEl.className = 'console-operations-field';
   enclosureFieldEl.appendChild(enclosureEl);
   locationEl.value = 'Africa Savanna';

   const controller = GuardiansTalkLocationFilter.createGuardiansTalkLocationFilterController({
      locationEl,
      talkNameEl,
      enclosureEl,
      loadTalks: async () => ({
         guardians_talks: [
            { name: 'Masai Giraffe', enclosure_names: ['Giraffe House', 'Outdoor'] },
            { name: 'Greater One-Horned Rhinoceros', enclosure_names: ['Indoor'] },
            { name: 'African Lion', enclosure_names: [] },
         ],
      }),
   });

   await controller.refresh();

   assert.deepEqual(
      talkNameEl.children.slice(1).map(option => option.value),
      ['African Lion', 'Greater One-Horned Rhinoceros', 'Masai Giraffe']
   );
   assert.equal(enclosureEl.disabled, true);
   assert.equal(enclosureFieldEl.classList.contains('is-invisible'), true);

   talkNameEl.value = 'Masai Giraffe';
   talkNameEl.dispatchEvent({ type: 'change' });

   assert.equal(enclosureEl.disabled, false);
   assert.equal(enclosureFieldEl.classList.contains('is-invisible'), false);
   assert.equal(enclosureEl.value, '');
   assert.deepEqual(
      enclosureEl.children.slice(1).map(option => option.value),
      ['Giraffe House', 'Outdoor']
   );
   assert.equal(enclosureEl.value, '');

   talkNameEl.value = 'Greater One-Horned Rhinoceros';
   talkNameEl.dispatchEvent({ type: 'change' });

   assert.equal(enclosureEl.disabled, true);
   assert.equal(enclosureEl.value, 'Indoor');
   assert.equal(enclosureFieldEl.classList.contains('is-invisible'), true);

   talkNameEl.value = 'African Lion';
   talkNameEl.dispatchEvent({ type: 'change' });

   assert.equal(enclosureEl.disabled, true);
   assert.equal(enclosureEl.value, '');
   assert.equal(enclosureFieldEl.classList.contains('is-invisible'), true);
});
