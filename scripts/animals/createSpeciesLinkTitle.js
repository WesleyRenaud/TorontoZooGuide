import { AnimalDisplayLines } from './animalDisplayLines.js';

function applyLinkDataset(element, dataset = {}) {
   Object.entries(dataset).forEach(([key, value]) => {
      if (value == null) {
         return;
      }

      element.dataset[key] = String(value);
   });
}

function bindSpeciesLinkActivation(linkEl, onClick) {
   linkEl.classList.add('species-link');
   linkEl.setAttribute('role', 'button');
   linkEl.setAttribute('tabindex', '0');

   const activate = (event) => {
      event.stopPropagation();
      onClick();
   };

   linkEl.addEventListener('click', activate);
   linkEl.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
         event.preventDefault();
         activate(event);
      }
   });
}

export function createSpeciesLinkTitleElement({
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
      applyLinkDataset(linkEl, dataset);

      if (typeof onClick === 'function') {
         bindSpeciesLinkActivation(linkEl, onClick);
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

export function createAnimalTitleLinkElement({
   species,
   enclosureName = null,
   className = '',
   tagName = 'div',
   onClick = null,
   dataset = {},
} = {}) {
   return createSpeciesLinkTitleElement({
      text: species,
      suffix: AnimalDisplayLines.formatAnimalTitleSuffix(enclosureName),
      className,
      tagName,
      onClick,
      dataset,
   });
}
