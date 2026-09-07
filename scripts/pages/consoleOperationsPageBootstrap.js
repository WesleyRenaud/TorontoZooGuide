import { ConsoleControllersBootstrap } from '../consoleOperations/bootstrap/consoleControllersBootstrap.js';
import { ConsoleOperationPanelsBootstrap } from '../consoleOperations/bootstrap/consoleOperationPanelsBootstrap.js';
import { DatePickers } from '../consoleOperations/bootstrap/datePickers.js';
import { PanelNavigator } from '../consoleOperations/shell/panelNavigator.js';

const CONSOLE_OPERATIONS_WORKSPACE_ID = 'consoleOperationsWorkspace';

export class ConsoleOperationsPageBootstrap {
   static getConsoleOperationsWorkspace() {
      return document.getElementById(CONSOLE_OPERATIONS_WORKSPACE_ID);
   }

   static createConsoleOperationSpecialControllers(refs) {
      return ConsoleControllersBootstrap.createConsoleSpecialControllers({
         guardiansTalks: refs.guardiansTalks,
         wildEncounters: refs.wildEncounters,
      });
   }

   static initConsoleOperationPanels(workspaceEl) {
      ConsoleOperationPanelsBootstrap.mountConsoleOperationPanels(workspaceEl);
   }

   static initConsoleOperationControllers(refs) {
      const {
         activatePanel,
         restorePanelFromUrl,
      } = PanelNavigator.createConsolePanelNavigator(document);

      ConsoleControllersBootstrap.wireConsoleOperationControllers({
         refs,
         activatePanel,
         ...ConsoleOperationsPageBootstrap.createConsoleOperationSpecialControllers(refs),
      });

      restorePanelFromUrl();
   }

   static initConsoleOperationDateControls(refs) {
      DatePickers.wireConsoleOperationDatePickers(refs);
   }
}
