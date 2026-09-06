import { Strings } from '../../../strings.js';

function createButton({
   className,
   text,
   ariaLabel = null,
} = {}) {
   const button = document.createElement('button');
   button.className = className;
   button.type = 'button';
   button.textContent = text;

   if (ariaLabel) {
      button.setAttribute('aria-label', ariaLabel);
   }

   return button;
}

export class Shell {
   static buildRegionSelectorShell() {
      const root = document.createElement('div');
      root.className = 'itin-overlay';

      const card = document.createElement('section');
      card.className = 'itin-card itin-card-tall';
      card.setAttribute('role', 'dialog');
      card.setAttribute('aria-modal', 'true');
      card.setAttribute('aria-label', Strings.itinerary.aria.selectRegionsAndExhibits);

      const topbar = document.createElement('div');
      topbar.className = 'itin-card-topbar itin-card-topbar-with-close';

      const topTitleEl = document.createElement('div');
      topTitleEl.className = 'itin-top-title';
      topTitleEl.textContent = Strings.itinerary.selectors.builderTitle;

      const closeButton = createButton({
         className: 'itin-close',
         text: Strings.common.closeSymbol,
         ariaLabel: Strings.itinerary.aria.closeBuilder,
      });

      topbar.append(topTitleEl, closeButton);

      const bodyEl = document.createElement('div');
      bodyEl.className = 'itin-card-body itin-card-body-tall';

      const heading = document.createElement('h1');
      heading.className = 'itin-h1';
      heading.textContent = Strings.itinerary.selectors.titleRegions;

      const resultsEl = document.createElement('div');
      resultsEl.className = 'itin-region-results itin-results';

      bodyEl.append(heading, resultsEl);

      const actions = document.createElement('div');
      actions.className = 'itin-card-actions-dual';

      const prevButton = createButton({
         className: 'itin-prev',
         text: Strings.animalsPage.back,
      });

      const actionsRight = document.createElement('div');
      actionsRight.className = 'itin-actions-right';

      const nextButton = createButton({
         className: 'itin-next',
         text: Strings.itinerary.actions.next,
      });

      const finishButton = createButton({
         className: 'itin-next itin-finish',
         text: Strings.itinerary.actions.finish,
      });

      actionsRight.append(nextButton, finishButton);
      actions.append(prevButton, actionsRight);
      card.append(topbar, bodyEl, actions);
      root.appendChild(card);

      return {
         root,
         resultsEl,
         prevButton,
         nextButton,
         finishButton,
         closeButton,
      };
   }
}
