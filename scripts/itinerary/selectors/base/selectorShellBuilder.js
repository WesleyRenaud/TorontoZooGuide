import { SelectorShellBuilderHelper } from './selectorShellBuilderHelper.js';
import { Strings } from '../../../strings.js';

export class SelectorShellBuilder {
   static buildSelectorShell({
      topTitle,
      h1,
      subtitle,
      hideNextButton = false,
   } = {}) {
      const root = document.createElement('div');
      root.className = 'itin-overlay';

      const card = document.createElement('section');
      card.className = 'itin-card itin-card-tall';
      card.setAttribute('role', 'dialog');
      card.setAttribute('aria-modal', 'true');

      const topbar = document.createElement('div');
      topbar.className = 'itin-card-topbar itin-card-topbar-with-close';

      const topTitleEl = document.createElement('div');
      topTitleEl.className = 'itin-top-title';
      topTitleEl.textContent = topTitle;

      const closeButton = SelectorShellBuilderHelper.createButton({
         className: 'itin-close',
         text: Strings.common.closeSymbol,
         ariaLabel: Strings.itinerary.aria.closeBuilder,
      });

      topbar.append(topTitleEl, closeButton);

      const bodyEl = document.createElement('div');
      bodyEl.className = 'itin-card-body itin-card-body-tall';

      const heading = document.createElement('h1');
      heading.className = 'itin-h1';
      heading.textContent = h1;

      const subtitleEl = document.createElement('p');
      subtitleEl.className = 'itin-subtitle';
      subtitleEl.textContent = subtitle;

      const inputEl = document.createElement('input');
      inputEl.className = 'itin-search-input';
      inputEl.type = 'text';
      inputEl.placeholder = Strings.itinerary.searchPlaceholder;
      inputEl.autocomplete = 'off';

      const resultsEl = document.createElement('div');
      resultsEl.className = 'itin-results';
      resultsEl.setAttribute('aria-live', 'polite');

      bodyEl.append(heading, subtitleEl, inputEl, resultsEl);

      const actions = document.createElement('div');
      actions.className = 'itin-card-actions-dual';

      const prevButton = SelectorShellBuilderHelper.createButton({
         className: 'itin-prev',
         text: Strings.itinerary.actions.previous,
      });

      const actionsRight = document.createElement('div');
      actionsRight.className = 'itin-actions-right';

      let nextButton = null;

      if (!hideNextButton) {
         nextButton = SelectorShellBuilderHelper.createButton({
            className: 'itin-next',
            text: Strings.itinerary.actions.next,
         });
         actionsRight.appendChild(nextButton);
      }

      const finishButton = SelectorShellBuilderHelper.createButton({
         className: 'itin-finish',
         text: Strings.itinerary.actions.finish,
      });

      actionsRight.appendChild(finishButton);
      actions.append(prevButton, actionsRight);
      card.append(topbar, bodyEl, actions);
      root.appendChild(card);

      return {
         root,
         bodyEl,
         inputEl,
         resultsEl,
         prevButton,
         nextButton,
         finishButton,
         closeButton,
      };
   }
}
