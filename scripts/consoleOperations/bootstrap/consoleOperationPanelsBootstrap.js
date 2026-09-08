import { ConsoleOperationPanelsBootstrapHelper } from './consoleOperationPanelsBootstrapHelper.js';

export class ConsoleOperationPanelsBootstrap {
   static mountConsoleOperationPanels(workspaceEl) {
      if (!workspaceEl) {
         return;
      }

      const doc = workspaceEl.ownerDocument || document;
      workspaceEl.replaceChildren(ConsoleOperationPanelsBootstrapHelper.createConsoleOperationPanelsFragment(doc));
   }
}
