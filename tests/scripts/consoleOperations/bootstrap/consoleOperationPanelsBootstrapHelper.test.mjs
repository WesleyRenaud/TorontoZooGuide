import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationPanelsBootstrapHelper } from '../../../../scripts/consoleOperations/bootstrap/consoleOperationPanelsBootstrapHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_GetPanelCreators_TestRegistry_ExpectFlattenedFunctions', () => {
   const creators = ConsoleOperationPanelsBootstrapHelper.getPanelCreators();

   assert.ok(Array.isArray(creators));
   assert.ok(creators.length >= 30);
   assert.ok(creators.every((createPanel) => typeof createPanel === 'function'));
});

test('Test_CreateConsoleOperationPanelsFragment_TestStubbedCreators_ExpectFragment', () => {
   const originalGet = ConsoleOperationPanelsBootstrapHelper.getPanelCreators;
   ConsoleOperationPanelsBootstrapHelper.getPanelCreators = () => [
      () => {
         const panel = document.createElement('section');
         panel.id = 'panel-a';
         panel.ownerDocument = document;
         return panel;
      },
      () => {
         const panel = document.createElement('section');
         panel.id = 'panel-b';
         panel.ownerDocument = document;
         return panel;
      },
   ];

   try {
      const fragment = ConsoleOperationPanelsBootstrapHelper.createConsoleOperationPanelsFragment();
      assert.equal(fragment.children.length, 2);
      assert.equal(fragment.children[0].id, 'panel-a');
      assert.equal(fragment.children[1].id, 'panel-b');
   } finally {
      ConsoleOperationPanelsBootstrapHelper.getPanelCreators = originalGet;
   }
});

test('Test_CreateConsoleOperationPanelsFragment_TestImportNode_ExpectImported', () => {
   const originalGet = ConsoleOperationPanelsBootstrapHelper.getPanelCreators;
   const imports = [];

   ConsoleOperationPanelsBootstrapHelper.getPanelCreators = () => [
      () => {
         const panel = document.createElement('section');
         panel.id = 'foreign-panel';
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
      assert.deepEqual(imports, [{ id: 'foreign-panel', deep: true }]);
      assert.equal(fragment.children[0].id, 'foreign-panel-imported');
   } finally {
      ConsoleOperationPanelsBootstrapHelper.getPanelCreators = originalGet;
      delete document.importNode;
   }
});
