import { Strings } from '../../strings.js';

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

export class DateSelectorView {
   static buildDateSelectorView(strings = Strings) {
      const root = document.createElement('div');
      root.className = 'itin-overlay';

      const card = document.createElement('section');
      card.className = 'itin-card';
      card.setAttribute('role', 'dialog');
      card.setAttribute('aria-modal', 'true');
      card.setAttribute('aria-label', strings.itinerary.selectors.builderTitle);

      const topbar = document.createElement('div');
      topbar.className = 'itin-card-topbar itin-card-topbar-with-close';

      const topTitle = document.createElement('div');
      topTitle.className = 'itin-top-title';
      topTitle.textContent = strings.itinerary.selectors.builderTitle;

      const closeButtonEl = createButton({
         className: 'itin-close',
         text: strings.common.closeSymbol,
         ariaLabel: strings.itinerary.aria.closeBuilder,
      });

      topbar.append(topTitle, closeButtonEl);

      const body = document.createElement('div');
      body.className = 'itin-card-body';

      const heading = document.createElement('h1');
      heading.className = 'itin-h1';
      heading.textContent = strings.itinerary.selectors.titleDate;

      const subtitle = document.createElement('p');
      subtitle.className = 'itin-subtitle';
      subtitle.textContent = strings.itinerary.selectors.visitDateSubtitle;

      const fieldLabel = document.createElement('div');
      fieldLabel.className = 'itin-field-label';
      fieldLabel.textContent = strings.itinerary.selectors.visitDate;

      const inputEl = document.createElement('input');
      inputEl.className = 'itin-date-input';
      inputEl.type = 'text';
      inputEl.inputMode = 'none';
      inputEl.autocomplete = 'off';
      inputEl.readOnly = true;

      body.append(heading, subtitle, fieldLabel, inputEl);

      const actions = document.createElement('div');
      actions.className = 'itin-card-actions';

      const actionsRight = document.createElement('div');
      actionsRight.className = 'itin-actions-right';

      const nextButtonEl = createButton({
         className: 'itin-next',
         text: strings.itinerary.actions.next,
      });

      const finishButtonEl = createButton({
         className: 'itin-next itin-finish',
         text: strings.itinerary.actions.finish,
      });

      actionsRight.append(nextButtonEl, finishButtonEl);
      actions.append(actionsRight);
      card.append(topbar, body, actions);
      root.appendChild(card);

      return {
         root,
         inputEl,
         nextButtonEl,
         finishButtonEl,
         closeButtonEl,
      };
   }
}
