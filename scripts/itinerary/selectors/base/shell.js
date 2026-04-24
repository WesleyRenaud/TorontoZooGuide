const CLOSE_BUTTON_LABEL = 'Close itinerary builder';
const SEARCH_PLACEHOLDER = 'Search...';
const PREVIOUS_BUTTON_TEXT = 'Previous';
const NEXT_BUTTON_TEXT = 'Next';
const FINISH_BUTTON_TEXT = 'Finish';

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

export function buildSelectorShell({
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

   const closeButton = createButton({
      className: 'itin-close',
      text: '×',
      ariaLabel: CLOSE_BUTTON_LABEL,
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
   inputEl.placeholder = SEARCH_PLACEHOLDER;
   inputEl.autocomplete = 'off';

   const resultsEl = document.createElement('div');
   resultsEl.className = 'itin-results';
   resultsEl.setAttribute('aria-live', 'polite');

   bodyEl.append(heading, subtitleEl, inputEl, resultsEl);

   const actions = document.createElement('div');
   actions.className = 'itin-card-actions-dual';

   const prevButton = createButton({
      className: 'itin-prev',
      text: PREVIOUS_BUTTON_TEXT,
   });

   const actionsRight = document.createElement('div');
   actionsRight.className = 'itin-actions-right';

   let nextButton = null;

   if (!hideNextButton) {
      nextButton = createButton({
         className: 'itin-next',
         text: NEXT_BUTTON_TEXT,
      });
      actionsRight.appendChild(nextButton);
   }

   const finishButton = createButton({
      className: 'itin-finish',
      text: FINISH_BUTTON_TEXT,
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
