import { buildSelectorShell } from './base/shell.js';

export function createSelectorElements({
   topTitle,
   h1,
   subtitle,
   hideNextButton,
} = {}) {
   const shell = buildSelectorShell({
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
