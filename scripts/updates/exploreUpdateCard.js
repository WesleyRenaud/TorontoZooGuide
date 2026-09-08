import { ExploreUpdateCardHelpers } from './exploreUpdateCardHelpers.js';
import { Strings } from '../strings.js';

export class ExploreUpdateCard {
   static createUpdateCard(update, isActive = false) {
      const cardEl = document.createElement('article');
      cardEl.className = 'explore-update-card';
      cardEl.hidden = !isActive;

      const metaEl = document.createElement('div');
      metaEl.className = 'explore-update-meta';
      metaEl.appendChild(ExploreUpdateCardHelpers.createUpdateTypeEl(update));

      const titleEl = document.createElement('h4');
      titleEl.className = 'explore-update-title';
      titleEl.textContent = update.title || Strings.labels.update;

      const descriptionEl = document.createElement('p');
      descriptionEl.className = 'explore-update-description';
      descriptionEl.textContent = update.description || '';

      cardEl.append(metaEl, titleEl, descriptionEl);
      return cardEl;
   }
}
