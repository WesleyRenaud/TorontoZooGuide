import { DetailImageBuilder } from '../assets/detailImageBuilder.js';
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

      const imageEl = document.createElement('img');
      imageEl.className = 'explore-event-image';
      imageEl.alt = event.name;
      imageEl.src = DetailImageBuilder.buildDetailImageSrc('events', event.name, {
         basePath: `../${DetailImageBuilder.BASE_PATH}`,
      });

      cardEl.append(ExploreEventCardHelper.createEventTitleEl(event), imageEl, metaEl, descriptionEl);
      return cardEl;
   }
}
