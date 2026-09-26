import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationPanelsBootstrapHelper } from '../../../../scripts/consoleOperations/bootstrap/consoleOperationPanelsBootstrapHelper.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_GetPanelCreators_TestRegistry_ExpectFlattenedFunctions', () => {
   const creators = ConsoleOperationPanelsBootstrapHelper.getPanelCreators();

   assert.ok(Array.isArray(creators));
   assert.ok(creators.length >= 30);
   assert.ok(creators.every((createPanel) => typeof createPanel === 'function'));
});


test('Test_CreateConsoleOperationPanelsFragment_TestStubbedCreators_ExpectFragment', () => {
   const firstId = 'panel-a';
   const secondId = 'panel-b';
   const originalGet = ConsoleOperationPanelsBootstrapHelper.getPanelCreators;
   ConsoleOperationPanelsBootstrapHelper.getPanelCreators = () => [
      () => {
         const panel = document.createElement('section');
         panel.id = firstId;
         panel.ownerDocument = document;
         return panel;
      },
      () => {
         const panel = document.createElement('section');
         panel.id = secondId;
         panel.ownerDocument = document;
         return panel;
      },
   ];

   try {
      const fragment = ConsoleOperationPanelsBootstrapHelper.createConsoleOperationPanelsFragment();

      assert.equal(fragment.children.length, 2);
      assert.equal(fragment.children.at(Position.FIRST).id, firstId);
      assert.equal(fragment.children.at(Position.LAST).id, secondId);
   } finally {
      ConsoleOperationPanelsBootstrapHelper.getPanelCreators = originalGet;
   }
});


test('Test_CreateConsoleOperationPanelsFragment_TestImportNode_ExpectImported', () => {
   const panelId = 'foreign-panel';
   const originalGet = ConsoleOperationPanelsBootstrapHelper.getPanelCreators;
   const imports = [];
   ConsoleOperationPanelsBootstrapHelper.getPanelCreators = () => [
      () => {
         const panel = document.createElement('section');
         panel.id = panelId;
         panel.ownerDocument = {};
         return panel;
      },
   ];
   document.importNode = (node, deep) => {
      imports.push({ id: node.id, deep });
      const cloned = document.createElement('section');
      cloned.id = `${node.id}-imported`;
      return cloned;
   };

   try {
      const fragment = ConsoleOperationPanelsBootstrapHelper.createConsoleOperationPanelsFragment();

      assert.deepEqual(imports, [{ id: panelId, deep: true }]);
      assert.equal(fragment.children.at(Position.FIRST).id, `${panelId}-imported`);
   } finally {
      ConsoleOperationPanelsBootstrapHelper.getPanelCreators = originalGet;
      delete document.importNode;
   }
});
