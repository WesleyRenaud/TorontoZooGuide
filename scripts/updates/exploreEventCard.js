import { ExploreEventCardHelpers } from './exploreEventCardHelpers.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

export class ExploreEventCard {
   static createEventCard(event, isActive = false) {
      const cardEl = document.createElement('article');
      cardEl.className = 'explore-update-card explore-event-card';
      cardEl.hidden = !isActive;

      const dateRangeEl = document.createElement('p');
      dateRangeEl.className = 'explore-event-date-range';
      dateRangeEl.textContent = VisitDateRules.formatLocalDateRange(event.start_date, event.end_date);

      const descriptionEl = document.createElement('p');
      descriptionEl.className = 'explore-update-description';
      descriptionEl.textContent = event.description || '';

      cardEl.append(ExploreEventCardHelpers.createEventTitleEl(event), dateRangeEl, descriptionEl);
      return cardEl;
   }
}
