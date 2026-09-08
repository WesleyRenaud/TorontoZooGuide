import { ConsoleOperationRefsCollector } from '../consoleOperations/bootstrap/consoleOperationRefsCollector.js';
import { ConsoleOperationsPageBootstrap } from './consoleOperationsPageBootstrap.js';

export class ConsoleOperationsBootstrap {
   static initConsoleOperationsPage() {
      const workspaceEl = ConsoleOperationsPageBootstrap.getConsoleOperationsWorkspace();

      if (!workspaceEl) {
         console.warn('[consoleOperations] missing #consoleOperationsWorkspace');
         return;
      }

      ConsoleOperationsPageBootstrap.initConsoleOperationPanels(workspaceEl);

      const refs = ConsoleOperationRefsCollector.collectConsoleOperationRefs(document);

      ConsoleOperationsPageBootstrap.initConsoleOperationControllers(refs);
      ConsoleOperationsPageBootstrap.initConsoleOperationDateControls(refs);
   }
}
