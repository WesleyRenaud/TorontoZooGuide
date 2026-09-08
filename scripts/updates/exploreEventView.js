import { ExploreEventCardHelper } from './exploreEventCardHelper.js';
import { VisitDateValidator } from '../visitDates/visitDateValidator.js';

export class ExploreEventView {
   static createEventCard(event, isActive = false) {
      const cardEl = document.createElement('article');
      cardEl.className = 'explore-update-card explore-event-card';
      cardEl.hidden = !isActive;

      const dateRangeEl = document.createElement('p');
      dateRangeEl.className = 'explore-event-date-range';
      dateRangeEl.textContent = VisitDateValidator.formatLocalDateRange(event.start_date, event.end_date);

      const descriptionEl = document.createElement('p');
      descriptionEl.className = 'explore-update-description';
      descriptionEl.textContent = event.description || '';

      cardEl.append(ExploreEventCardHelper.createEventTitleEl(event), dateRangeEl, descriptionEl);
      return cardEl;
   }
}
