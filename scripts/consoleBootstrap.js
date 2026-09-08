import { ConsoleOperationsBootstrap } from './pages/consoleOperationsBootstrap.js';

export class ConsoleBootstrap {
   static bind() {
      document.addEventListener('DOMContentLoaded', () => {
         ConsoleOperationsBootstrap.initConsoleOperationsPage();
      });
   }

   static {
      ConsoleBootstrap.bind();
   }
}
