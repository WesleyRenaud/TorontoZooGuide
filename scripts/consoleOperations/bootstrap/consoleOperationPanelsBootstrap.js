import { ConsoleOperationPanelsBootstrapHelpers } from './consoleOperationPanelsBootstrapHelpers.js';

export class ConsoleOperationPanelsBootstrap {
   static mountConsoleOperationPanels(workspaceEl) {
      if (!workspaceEl) {
         return;
      }

      const doc = workspaceEl.ownerDocument || document;
      workspaceEl.replaceChildren(ConsoleOperationPanelsBootstrapHelpers.createConsoleOperationPanelsFragment(doc));
   }
}
