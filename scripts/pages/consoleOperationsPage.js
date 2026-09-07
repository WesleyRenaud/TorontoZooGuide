import { ConsoleControllersBootstrap } from '../consoleOperations/bootstrap/consoleControllersBootstrap.js';
import { ConsoleOperationPanelsBootstrap } from '../consoleOperations/bootstrap/consoleOperationPanelsBootstrap.js';
import { ConsoleOperationRefsCollector } from '../consoleOperations/bootstrap/consoleOperationRefsCollector.js';
import { DatePickers } from '../consoleOperations/bootstrap/datePickers.js';
import { PanelNavigator } from '../consoleOperations/shell/panelNavigator.js';

const CONSOLE_OPERATIONS_WORKSPACE_ID = 'consoleOperationsWorkspace';

function getConsoleOperationsWorkspace() {
   return document.getElementById(CONSOLE_OPERATIONS_WORKSPACE_ID);
}

function createConsoleOperationSpecialControllers(refs) {
   return ConsoleControllersBootstrap.createConsoleSpecialControllers({
      guardiansTalks: refs.guardiansTalks,
      wildEncounters: refs.wildEncounters,
   });
}

function initConsoleOperationPanels(workspaceEl) {
   ConsoleOperationPanelsBootstrap.mountConsoleOperationPanels(workspaceEl);
}

function initConsoleOperationControllers(refs) {
   const {
      activatePanel,
      restorePanelFromUrl,
   } = PanelNavigator.createConsolePanelNavigator(document);

   ConsoleControllersBootstrap.wireConsoleOperationControllers({
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

      const refs = ConsoleOperationRefsCollector.collectConsoleOperationRefs(document);

      initConsoleOperationControllers(refs);
      initConsoleOperationDateControls(refs);
   }
}
