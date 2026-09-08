import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkLocationFilter } from '../../../../../scripts/consoleOperations/guardiansTalks/controllers/guardiansTalkLocationFilter.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
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
