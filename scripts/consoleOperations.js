import { ConsoleOperationsPage } from './pages/consoleOperationsPage.js';

export class ConsoleOperations {
   static bind() {
      document.addEventListener('DOMContentLoaded', () => {
         ConsoleOperationsPage.initConsoleOperationsPage();
      });
   }
}

ConsoleOperations.bind();
