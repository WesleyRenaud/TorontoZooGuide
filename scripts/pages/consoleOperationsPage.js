import {
   createConsoleSpecialControllers,
   wireConsoleOperationControllers,
} from '../consoleOperations/bootstrap/controllers.js';
import { DatePickers } from '../consoleOperations/bootstrap/datePickers.js';
import { Panels } from '../consoleOperations/bootstrap/panels.js';
import { collectConsoleOperationRefs } from '../consoleOperations/bootstrap/refs.js';
import { PanelNavigator } from '../consoleOperations/shell/panelNavigator.js';

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
   Panels.mountConsoleOperationPanels(workspaceEl);
}

function initConsoleOperationControllers(refs) {
   const {
      activatePanel,
      restorePanelFromUrl,
   } = PanelNavigator.createConsolePanelNavigator(document);

   wireConsoleOperationControllers({
      refs,
      activatePanel,
      ...createConsoleOperationSpecialControllers(refs),
   });

   restorePanelFromUrl();
}

function initConsoleOperationDateControls(refs) {
   DatePickers.wireConsoleOperationDatePickers(refs);
}

export class ConsoleOperationsPage {
   static initConsoleOperationsPage() {
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
}
