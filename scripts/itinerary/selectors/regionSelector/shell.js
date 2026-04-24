const DIALOG_LABEL = 'Select regions and exhibits';
const TOP_TITLE = 'Itinerary Builder';
const CLOSE_BUTTON_LABEL = 'Close itinerary builder';
const TITLE = 'Add Animals by Region';
const PREVIOUS_BUTTON_TEXT = 'Back';
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

export function buildRegionSelectorShell() {
   const root = document.createElement('div');
   root.className = 'itin-overlay';

   const card = document.createElement('section');
   card.className = 'itin-card itin-card-tall';
   card.setAttribute('role', 'dialog');
   card.setAttribute('aria-modal', 'true');
   card.setAttribute('aria-label', DIALOG_LABEL);

   const topbar = document.createElement('div');
   topbar.className = 'itin-card-topbar itin-card-topbar-with-close';

   const topTitleEl = document.createElement('div');
   topTitleEl.className = 'itin-top-title';
   topTitleEl.textContent = TOP_TITLE;

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
   heading.textContent = TITLE;

   const resultsEl = document.createElement('div');
   resultsEl.className = 'itin-region-results itin-results';

   bodyEl.append(heading, resultsEl);

   const actions = document.createElement('div');
   actions.className = 'itin-card-actions-dual';

   const prevButton = createButton({
      className: 'itin-prev',
      text: PREVIOUS_BUTTON_TEXT,
   });

   const actionsRight = document.createElement('div');
   actionsRight.className = 'itin-actions-right';

   const nextButton = createButton({
      className: 'itin-next',
      text: NEXT_BUTTON_TEXT,
   });

   const finishButton = createButton({
      className: 'itin-next itin-finish',
      text: FINISH_BUTTON_TEXT,
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
