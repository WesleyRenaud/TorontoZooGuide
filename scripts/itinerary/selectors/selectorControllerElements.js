import { Shell } from './base/shell.js';

export class SelectorControllerElements {
   static createSelectorElements({
      topTitle,
      h1,
      subtitle,
      hideNextButton,
   } = {}) {
      const shell = Shell.buildSelectorShell({
         topTitle,
         h1,
         subtitle,
         hideNextButton,
      });

      return {
         rootEl: shell.root,
         bodyEl: shell.bodyEl,
         inputEl: shell.inputEl,
         resultsEl: shell.resultsEl,
         prevButtonEl: shell.prevButton,
         nextButtonEl: shell.nextButton,
         finishButtonEl: shell.finishButton,
         closeButtonEl: shell.closeButton,
      };
   }
}
