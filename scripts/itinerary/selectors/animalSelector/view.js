import { createWarningIcon } from '../../../assets/warningIcon.js';
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
