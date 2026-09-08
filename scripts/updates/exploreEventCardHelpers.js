import { ValueNormalizer } from '../api/valueNormalizer.js';
import { Strings } from '../strings.js';

export class ExploreEventCardHelpers {
   static createEventTitleEl(event) {
      const titleEl = document.createElement('h4');
      titleEl.className = 'explore-update-title';

      const name = event.name || Strings.map.events.title;
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
}
