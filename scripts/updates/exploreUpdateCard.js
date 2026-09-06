import { Strings } from '../strings.js';

function createUpdateTypeEl(update) {
   const typeEl = document.createElement('span');
   typeEl.className = `explore-update-type explore-update-type-${String(update.type || '')
      .toLowerCase()
      .replaceAll(' ', '-')}`;
   typeEl.textContent = update.type || Strings.labels.update;
   return typeEl;
}

export class ExploreUpdateCard {
   static createUpdateCard(update, isActive = false) {
      const cardEl = document.createElement('article');
      cardEl.className = 'explore-update-card';
      cardEl.hidden = !isActive;

      const metaEl = document.createElement('div');
      metaEl.className = 'explore-update-meta';
      metaEl.appendChild(createUpdateTypeEl(update));

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
