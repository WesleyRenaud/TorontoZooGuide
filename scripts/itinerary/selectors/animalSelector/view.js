import {
   buildAnimalImageSrc,
   getAnimalLikelihoodLevel,
   getAnimalSpecies,
   getAnimalSubtitle,
} from './model.js';

function createLikelihoodWarning(level) {
   if (!level) {
      return null;
   }

   const warning = document.createElement('span');
   warning.className = `itin-likelihood-warning ${level}`;
   warning.innerHTML = `
      <svg viewBox="0 0 24 24" class="itin-warning-icon">
         <path d="M12 2L1 21h22L12 2z"></path>
         <rect x="11" y="9" width="2" height="6" fill="black"></rect>
         <circle cx="12" cy="18" r="1.6" fill="black"></circle>
      </svg>
   `;
   warning.title = level === 'low'
      ? 'Very low chance of seeing this animal'
      : 'This animal may be off display';

   return warning;
}

export function renderAnimalSelectorRowLeft(row) {
   const species = getAnimalSpecies(row) || 'Animal';
   const subtitle = getAnimalSubtitle(row);
   const imageSrc = buildAnimalImageSrc(row);

   const content = document.createElement('div');
   content.className = 'itin-animal-content';

   const thumbWrap = document.createElement('div');
   thumbWrap.className = 'itin-animal-thumb';

   if (imageSrc) {
      const img = document.createElement('img');
      img.className = 'itin-animal-thumb-img';
      img.loading = 'lazy';
      img.alt = `${species} photo`;
      img.src = imageSrc;

      img.addEventListener('error', () => {
         thumbWrap.classList.add('is-placeholder');
         img.remove();
      });

      thumbWrap.appendChild(img);
   } else {
      thumbWrap.classList.add('is-placeholder');
   }

   const left = document.createElement('div');
   left.className = 'animal-result-left';

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

   left.appendChild(titleWrap);

   if (subtitle) {
      const subtitleEl = document.createElement('div');
      subtitleEl.className = 'animal-result-exhibit';
      subtitleEl.textContent = subtitle;
      left.appendChild(subtitleEl);
   }

   content.appendChild(thumbWrap);
   content.appendChild(left);

   return content;
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
   text.textContent = 'Include off-display animals';

   checkbox.addEventListener('change', () => {
      onChange?.(checkbox.checked);
      rerunSearch?.();
   });

   label.appendChild(checkbox);
   label.appendChild(text);
   toggleWrap.appendChild(label);

   bodyEl.insertBefore(toggleWrap, bodyEl.querySelector('.itin-search-input'));
}
