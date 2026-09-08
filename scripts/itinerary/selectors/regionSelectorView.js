import { RegionSelectorShellBuilder } from './regionSelector/regionSelectorShellBuilder.js';

export class RegionSelectorView {
   static createRegionSelectorElements() {
      const shell = RegionSelectorShellBuilder.buildRegionSelectorShell();

      return {
         rootEl: shell.root,
         resultsEl: shell.resultsEl,
         prevButtonEl: shell.prevButton,
         nextButtonEl: shell.nextButton,
         finishButtonEl: shell.finishButton,
         closeButtonEl: shell.closeButton,
      };
   }
}
