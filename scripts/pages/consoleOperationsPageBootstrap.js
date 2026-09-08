import { ConsoleControllersBootstrap } from '../consoleOperations/bootstrap/consoleControllersBootstrap.js';
import { ConsoleOperationPanelsBootstrap } from '../consoleOperations/bootstrap/consoleOperationPanelsBootstrap.js';
import { DateFactory } from '../consoleOperations/bootstrap/dateFactory.js';
import { PanelNavigator } from '../consoleOperations/shell/panelNavigator.js';

export class ConsoleOperationsPageBootstrap {
   static CONSOLE_OPERATIONS_WORKSPACE_ID = 'consoleOperationsWorkspace';

   static getConsoleOperationsWorkspace() {
      return document.getElementById(ConsoleOperationsPageBootstrap.CONSOLE_OPERATIONS_WORKSPACE_ID);
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
      DateFactory.wireConsoleOperationDatePickers(refs);
   }
}
