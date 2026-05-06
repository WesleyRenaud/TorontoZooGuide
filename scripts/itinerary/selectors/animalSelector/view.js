import {
   createSelectorRowContent,
   createSelectorTextColumn,
} from '../base/resultRenderer.js';
import {
   buildAnimalImageSrc,
   getAnimalLikelihoodLevel,
   getAnimalSpecies,
   getAnimalSubtitle,
} from './model.js';
import { APP_STRINGS } from '../../../strings.js';

const SVG_NS = 'http://www.w3.org/2000/svg';

function createSvgNode(tagName, attributes = {}) {
   const node = document.createElementNS(SVG_NS, tagName);

   Object.entries(attributes).forEach(([key, value]) => {
      node.setAttribute(key, String(value));
   });

   return node;
}

function createWarningIcon() {
   const svg = createSvgNode('svg', {
      viewBox: '0 0 24 24',
      class: 'itin-warning-icon',
   });

   svg.append(
      createSvgNode('path', {
         d: 'M12 2L1 21h22L12 2z',
      }),
      createSvgNode('rect', {
         x: '11',
         y: '9',
         width: '2',
         height: '6',
         fill: 'black',
      }),
      createSvgNode('circle', {
         cx: '12',
         cy: '18',
         r: '1.6',
         fill: 'black',
      })
   );

   return svg;
}

function createLikelihoodWarning(level) {
   if (!level) {
      return null;
   }

   const warning = document.createElement('span');
   warning.className = `itin-likelihood-warning ${level}`;
   warning.appendChild(createWarningIcon());
   warning.title = level === 'low'
      ? APP_STRINGS.itinerary.selectors.lowVisibilityHint
      : APP_STRINGS.itinerary.confirmation.animalMayBeOffDisplay;

   return warning;
}

export function renderAnimalSelectorRowLeft(row) {
   const species = getAnimalSpecies(row) || 'Animal';
   const subtitle = getAnimalSubtitle(row);
   const imageSrc = buildAnimalImageSrc(row);

   const titleWrap = document.createElement('div');
   titleWrap.className = 'itin-animal-title-wrap';

   const titleEl = document.createElement('div');
   titleEl.className = 'animal-result-species';
   titleEl.textContent = species;

   titleWrap.appendChild(titleEl);

   const warning = createLikelihoodWarning(getAnimalLikelihoodLevel(row));

   if (warning) {
      titleWrap.appendChild(warning);
   }

   return createSelectorRowContent({
      imageSrc,
      imageAlt: APP_STRINGS.itinerary.itemPhoto(species),
      textColumnEl: createSelectorTextColumn({
         subtitle,
         titleNode: titleWrap,
      }),
   });
}

export function renderIncludeOffDisplayToggle({ bodyEl, rerunSearch, onChange }) {
   const toggleWrap = document.createElement('div');
   toggleWrap.className = 'itin-selector-toggle-wrap';

   const label = document.createElement('label');
   label.className = 'toggle-row itin-selector-toggle-row';

   const checkbox = document.createElement('input');
   checkbox.type = 'checkbox';
   checkbox.checked = false;

   const text = document.createElement('span');
   text.textContent = APP_STRINGS.itinerary.selectors.includeOffDisplayAnimals;

   checkbox.addEventListener('change', () => {
      onChange?.(checkbox.checked);
      rerunSearch?.();
   });

   label.appendChild(checkbox);
   label.appendChild(text);
   toggleWrap.appendChild(label);

   bodyEl.insertBefore(toggleWrap, bodyEl.querySelector('.itin-search-input'));
}
