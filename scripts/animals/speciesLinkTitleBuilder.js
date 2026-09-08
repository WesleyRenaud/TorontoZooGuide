import { AnimalDisplayFormatter } from './animalDisplayFormatter.js';
import { CreateSpeciesLinkTitleHelper } from './createSpeciesLinkTitleHelper.js';

export class SpeciesLinkTitleBuilder {
   static createSpeciesLinkTitleElement({
      text,
      suffix = '',
      className = '',
      tagName = 'div',
      onClick = null,
      dataset = {},
   } = {}) {
      const titleEl = document.createElement(tagName);

      if (className) {
         titleEl.className = className;
      }

      const hasDataset = Object.values(dataset).some((value) => value != null);
      const isLink = typeof onClick === 'function' || hasDataset;
      const linkEl = document.createElement('span');
      linkEl.textContent = text;

      if (isLink) {
         CreateSpeciesLinkTitleHelper.applyLinkDataset(linkEl, dataset);

         if (typeof onClick === 'function') {
            CreateSpeciesLinkTitleHelper.bindSpeciesLinkActivation(linkEl, onClick);
         }
         else {
            linkEl.classList.add('species-link');
            linkEl.setAttribute('role', 'button');
            linkEl.setAttribute('tabindex', '0');
         }
      }

      titleEl.appendChild(linkEl);

      if (suffix) {
         titleEl.appendChild(document.createTextNode(suffix));
      }

      return titleEl;
   }

   static createAnimalTitleLinkElement({
      species,
      enclosureName = null,
      className = '',
      tagName = 'div',
      onClick = null,
      dataset = {},
   } = {}) {
      return SpeciesLinkTitleBuilder.createSpeciesLinkTitleElement({
         text: species,
         suffix: AnimalDisplayFormatter.formatAnimalTitleSuffix(enclosureName),
         className,
         tagName,
         onClick,
         dataset,
      });
   }
}
