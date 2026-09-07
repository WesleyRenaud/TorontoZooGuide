import { SelectorShellBuilder } from './base/selectorShellBuilder.js';

export class SelectorControllerElements {
   static createSelectorElements({
      topTitle,
      h1,
      subtitle,
      hideNextButton,
   } = {}) {
      const shell = SelectorShellBuilder.buildSelectorShell({
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
