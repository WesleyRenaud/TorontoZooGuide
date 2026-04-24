import { mountConsoleOperationPanels } from '../consoleOperations/bootstrap/panels.js';
import { collectConsoleOperationRefs } from '../consoleOperations/bootstrap/refs.js';
import {
   createConsoleSpecialControllers,
   wireConsoleOperationControllers,
} from '../consoleOperations/bootstrap/controllers.js';
import { wireConsoleOperationDatePickers } from '../consoleOperations/bootstrap/datePickers.js';
import { createConsolePanelNavigator } from '../consoleOperations/shell/panelNavigator.js';

const CONSOLE_OPERATIONS_WORKSPACE_ID = 'consoleOperationsWorkspace';

function getConsoleOperationsWorkspace() {
   return document.getElementById(CONSOLE_OPERATIONS_WORKSPACE_ID);
}

function createConsoleOperationSpecialControllers(refs) {
   return createConsoleSpecialControllers({
      guardiansTalks: refs.guardiansTalks,
      wildEncounters: refs.wildEncounters,
   });
}

function initConsoleOperationPanels(workspaceEl) {
   mountConsoleOperationPanels(workspaceEl);
}

function initConsoleOperationControllers(refs) {
   const { activatePanel } = createConsolePanelNavigator(document);

   wireConsoleOperationControllers({
      refs,
      activatePanel,
      ...createConsoleOperationSpecialControllers(refs),
   });
}

function initConsoleOperationDateControls(refs) {
   wireConsoleOperationDatePickers(refs);
}

export function initConsoleOperationsPage() {
   const workspaceEl = getConsoleOperationsWorkspace();

   if (!workspaceEl) {
      console.warn('[consoleOperations] missing #consoleOperationsWorkspace');
      return;
   }

   initConsoleOperationPanels(workspaceEl);

   const refs = collectConsoleOperationRefs(document);

   initConsoleOperationControllers(refs);
   initConsoleOperationDateControls(refs);
}
