import { ItinerarySettingsWarningCopy } from './itinerarySettingsWarningCopy.js';
import { Strings } from '../../strings.js';

export class ItinerarySettingsView {
   static buildItinerarySettingsView({
      statuses = [],
      strings = Strings,
   } = {}) {
      const root = document.createElement('div');
      root.className = 'itin-overlay itin-settings-overlay';

      const card = document.createElement('section');
      card.className = 'itin-card itin-card-tall';
      card.setAttribute('role', 'dialog');
      card.setAttribute('aria-modal', 'true');
      card.setAttribute('aria-label', strings.itinerary.settings.title);

      const topbar = document.createElement('div');
      topbar.className = 'itin-card-topbar itin-card-topbar-with-close';

      const topTitle = document.createElement('div');
      topTitle.className = 'itin-top-title';
      topTitle.textContent = strings.itinerary.settings.title;

      const closeButtonEl = document.createElement('button');
      closeButtonEl.className = 'itin-close';
      closeButtonEl.type = 'button';
      closeButtonEl.textContent = strings.common.closeSymbol;
      closeButtonEl.setAttribute('aria-label', strings.itinerary.settings.closeAriaLabel);

      topbar.append(topTitle, closeButtonEl);

      const body = document.createElement('div');
      body.className = 'itin-card-body itin-card-body-tall';

      const heading = document.createElement('h1');
      heading.className = 'itin-h1';
      heading.textContent = strings.itinerary.settings.heading;

      const subtitle = document.createElement('p');
      subtitle.className = 'itin-subtitle';
      subtitle.textContent = strings.itinerary.settings.subtitle;

      const listEl = document.createElement('div');
      listEl.className = 'itin-settings-list';

      const checkboxEls = [];

      ItinerarySettingsWarningCopy.sortSuppressableStatuses(statuses).forEach((entry) => {
         const copy = ItinerarySettingsWarningCopy.copyForStatus(entry.status, strings);
         const rowEl = document.createElement('label');
         rowEl.className = 'itin-settings-row';

         const checkboxEl = document.createElement('input');
         checkboxEl.type = 'checkbox';
         checkboxEl.className = 'itin-settings-checkbox';
         checkboxEl.checked = !entry.isSuppressed;
         checkboxEl.dataset.status = entry.status;

         const copyEl = document.createElement('span');
         copyEl.className = 'itin-settings-row-copy';

         const titleEl = document.createElement('span');
         titleEl.className = 'itin-settings-row-title';
         titleEl.textContent = copy.title;

         const descriptionEl = document.createElement('span');
         descriptionEl.className = 'itin-settings-row-description';
         descriptionEl.textContent = copy.description;

         copyEl.append(titleEl, descriptionEl);
         rowEl.append(checkboxEl, copyEl);
         listEl.appendChild(rowEl);
         checkboxEls.push(checkboxEl);
      });

      body.append(heading, subtitle, listEl);

      const actions = document.createElement('div');
      actions.className = 'itin-card-actions';

      const actionsRight = document.createElement('div');
      actionsRight.className = 'itin-actions-right';

      const saveButtonEl = document.createElement('button');
      saveButtonEl.className = 'itin-finish';
      saveButtonEl.type = 'button';
      saveButtonEl.textContent = strings.actions.save;

      actionsRight.appendChild(saveButtonEl);
      actions.appendChild(actionsRight);
      card.append(topbar, body, actions);
      root.appendChild(card);

      return {
         root,
         closeButtonEl,
         saveButtonEl,
         checkboxEls,
      };
   }
}
