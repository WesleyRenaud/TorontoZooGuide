import { el } from '../dom.js';

export function createRemovedItemsPopupLayout({ isEmptyItinerary = false } = {}) {
   const root = el('div', 'tzg-popup');
   const overlay = el('div', 'itin-overlay');

   const card = el('section', 'itin-card itin-removed-popup-card');

   const topbar = el('div', 'itin-card-topbar itin-card-topbar-with-close');
   topbar.appendChild(
      el('div', 'itin-top-title', 'Itinerary Updated')
   );

   const closeBtn = el('button', 'itin-close', '×');
   closeBtn.type = 'button';
   topbar.appendChild(closeBtn);

   const body = el('div', 'itin-card-body tzg-popup-body itin-removed-popup-body');
   const content = el(
      'div',
      isEmptyItinerary
         ? 'itin-removed-popup-content itin-removed-popup-content-empty'
         : 'itin-removed-popup-content'
   );

   content.appendChild(
      el(
         'div',
         'itin-h1',
         isEmptyItinerary ? 'Your itinerary is now empty' : 'Some itinerary details changed'
      )
   );

   content.appendChild(
      el(
         'div',
         'itin-subtitle',
         isEmptyItinerary
            ? 'None of your selected items are available on the new date. You can view alternatives below.'
            : 'Some itinerary items changed for your new date. Review the updates below.'
      )
   );

   body.appendChild(content);

   const actions = el('div', 'itin-card-actions');

   const okBtn = el('button', 'itin-finish', isEmptyItinerary ? 'Accept' : 'Okay');
   okBtn.type = 'button';
   actions.appendChild(okBtn);

   card.appendChild(topbar);
   card.appendChild(body);
   card.appendChild(actions);

   overlay.appendChild(card);
   root.appendChild(overlay);

   return {
      root,
      overlay,
      content,
      closeBtn,
      okBtn,
   };
}
