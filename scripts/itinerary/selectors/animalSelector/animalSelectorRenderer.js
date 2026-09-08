import { CreateSpeciesLinkTitle } from '../../../animals/createSpeciesLinkTitle.js';
import { AnimalSelectorModel } from './animalSelectorModel.js';
import { AnimalSelectorRendererHelpers } from './animalSelectorRendererHelpers.js';
import { ResultRenderer } from '../base/resultRenderer.js';
import { Strings } from '../../../strings.js';

export class AnimalSelectorRenderer {
   static renderAnimalSelectorRowLeft(row) {
      const species = AnimalSelectorModel.getAnimalSpecies(row);
      const subtitle = AnimalSelectorModel.getAnimalSubtitle(row);
      const imageSrc = AnimalSelectorModel.buildAnimalImageSrc(row);

      const titleWrap = document.createElement('div');
      titleWrap.className = 'itin-animal-title-wrap';

      const titleEl = CreateSpeciesLinkTitle.createAnimalTitleLinkElement({
         species,
         enclosureName: AnimalSelectorModel.getAnimalEnclosureName(row),
         className: 'animal-result-species',
      });

      titleWrap.appendChild(titleEl);

      const warning = AnimalSelectorRendererHelpers.createLikelihoodWarning(
         AnimalSelectorModel.getAnimalLikelihoodLevel(row)
      );

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
