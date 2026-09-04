import { ValueNormalizer } from '../api/valueNormalizer.js';
import { APP_STRINGS } from '../strings.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

function createEventTitleEl(event) {
   const titleEl = document.createElement('h4');
   titleEl.className = 'explore-update-title';

   const name = event.name || APP_STRINGS.map.events.title;
   const location = ValueNormalizer.asTrimmedString(event.location);
   const link = ValueNormalizer.asTrimmedString(event.link);

   if (link) {
      const linkEl = document.createElement('a');
      linkEl.className = 'explore-event-title-link';
      linkEl.href = link;
      linkEl.target = '_blank';
      linkEl.rel = 'noopener noreferrer';
      linkEl.textContent = name;
      titleEl.appendChild(linkEl);
   }
   else {
      titleEl.appendChild(document.createTextNode(name));
   }

   if (location) {
      titleEl.appendChild(document.createTextNode(` • ${location}`));
   }

   return titleEl;
}

export function createEventCard(event, isActive = false) {
   const cardEl = document.createElement('article');
   cardEl.className = 'explore-update-card explore-event-card';
   cardEl.hidden = !isActive;

   const dateRangeEl = document.createElement('p');
   dateRangeEl.className = 'explore-event-date-range';
   dateRangeEl.textContent = VisitDateRules.formatLocalDateRange(event.start_date, event.end_date);

   const descriptionEl = document.createElement('p');
   descriptionEl.className = 'explore-update-description';
   descriptionEl.textContent = event.description || '';

   cardEl.append(createEventTitleEl(event), dateRangeEl, descriptionEl);
   return cardEl;
}
