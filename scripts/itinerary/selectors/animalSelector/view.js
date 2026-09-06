import { CreateSpeciesLinkTitle } from '../../../animals/createSpeciesLinkTitle.js';
import { WarningIcon } from '../../../assets/warningIcon.js';
import { ResultRenderer } from '../base/resultRenderer.js';
import {
   buildAnimalImageSrc,
   getAnimalEnclosureName,
   getAnimalLikelihoodLevel,
   getAnimalSpecies,
   getAnimalSubtitle,
} from './model.js';
import { Strings } from '../../../strings.js';

function createLikelihoodWarning(level) {
   if (!level) {
      return null;
   }

   const warning = document.createElement('span');
   warning.className = `itin-likelihood-warning ${level}`;
   warning.appendChild(WarningIcon.createWarningIcon());
   warning.title = level === 'low'
      ? Strings.itinerary.selectors.lowVisibilityHint
      : Strings.itinerary.confirmation.animalMayBeOffDisplay;

   return warning;
}

export class View {
   static renderAnimalSelectorRowLeft(row) {
      const species = getAnimalSpecies(row);
      const subtitle = getAnimalSubtitle(row);
      const imageSrc = buildAnimalImageSrc(row);

      const titleWrap = document.createElement('div');
      titleWrap.className = 'itin-animal-title-wrap';

      const titleEl = CreateSpeciesLinkTitle.createAnimalTitleLinkElement({
         species,
         enclosureName: getAnimalEnclosureName(row),
         className: 'animal-result-species',
      });

      titleWrap.appendChild(titleEl);

      const warning = createLikelihoodWarning(getAnimalLikelihoodLevel(row));

      if (warning) {
         titleWrap.appendChild(warning);
      }

      return ResultRenderer.createSelectorRowContent({
         imageSrc,
         imageAlt: Strings.itinerary.itemPhoto(species),
         textColumnEl: ResultRenderer.createSelectorTextColumn({
            subtitle,
            titleNode: titleWrap,
         }),
      });

   }

   static renderIncludeOffDisplayToggle({ bodyEl, rerunSearch, onChange }) {
      const toggleWrap = document.createElement('div');
      toggleWrap.className = 'itin-selector-toggle-wrap';

      const label = document.createElement('label');
      label.className = 'toggle-row itin-selector-toggle-row';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = false;

      const text = document.createElement('span');
      text.textContent = Strings.itinerary.selectors.includeOffDisplayAnimals;

      checkbox.addEventListener('change', () => {
         onChange?.(checkbox.checked);
         rerunSearch?.();
      });

      label.appendChild(checkbox);
      label.appendChild(text);
      toggleWrap.appendChild(label);

      bodyEl.insertBefore(toggleWrap, bodyEl.querySelector('.itin-search-input'));
   }
}
