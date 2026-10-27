import { ExploreEventCardHelper } from './exploreEventCardHelper.js';
import { VisitDateFormatter } from '../visitDates/visitDateFormatter.js';

export class ExploreEventView {
   static createEventCard(event, isActive = false) {
      const cardEl = document.createElement('article');
      cardEl.className = 'explore-update-card explore-event-card';
      cardEl.hidden = !isActive;

      const dateRangeEl = document.createElement('span');
      dateRangeEl.className = 'explore-update-type explore-event-date-range';
      dateRangeEl.textContent = VisitDateFormatter.formatRange(event.start_date, event.end_date);

      const metaEl = document.createElement('div');
      metaEl.className = 'explore-update-meta';
      metaEl.appendChild(dateRangeEl);

      const descriptionEl = document.createElement('p');
      descriptionEl.className = 'explore-update-description';
      descriptionEl.textContent = event.description || '';

      cardEl.append(metaEl, ExploreEventCardHelper.createEventTitleEl(event), descriptionEl);
      return cardEl;
   }
}
