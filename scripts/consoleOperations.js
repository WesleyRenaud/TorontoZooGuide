import { mountConsoleOperationPanels } from './consoleOperations/bootstrap/panels.js';
import { collectConsoleOperationRefs } from './consoleOperations/bootstrap/refs.js';
import {
   createConsoleSpecialControllers,
   wireConsoleOperationControllers
} from './consoleOperations/bootstrap/controllers.js';
import { wireConsoleOperationDatePickers } from './consoleOperations/bootstrap/datePickers.js';
import { createConsolePanelNavigator } from './consoleOperations/shell/panelNavigator.js';

document.addEventListener('DOMContentLoaded', () => {

   const workspaceEl = document.getElementById('consoleOperationsWorkspace');

   if (!workspaceEl) {
      console.warn('[consoleOperations] missing #consoleOperationsWorkspace');
      return;
   }

   mountConsoleOperationPanels(workspaceEl);

   const refs = collectConsoleOperationRefs(document);
   const { activatePanel, hidePanels } = createConsolePanelNavigator(document);

   const specialControllers = createConsoleSpecialControllers({
      guardiansTalks: refs.guardiansTalks,
      wildEncounters: refs.wildEncounters,
   });

   wireConsoleOperationControllers({
      refs,
      activatePanel,
      hidePanels,
      ...specialControllers,
   });

   wireConsoleOperationDatePickers(refs);

});
