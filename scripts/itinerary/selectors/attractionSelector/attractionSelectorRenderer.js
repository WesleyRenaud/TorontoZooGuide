import { Strings } from '../../../strings.js';

export class AttractionSelectorRenderer {
   static renderIncludeClosedAttractionsToggle({
      bodyEl,
      rerunSearch,
      onChange,
   } = {}) {
      const toggleWrap = document.createElement('div');
      toggleWrap.className = 'itin-selector-toggle-wrap';

      const label = document.createElement('label');
      label.className = 'toggle-row itin-selector-toggle-row';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = false;

      const text = document.createElement('span');
      text.textContent = Strings.map.toggleLabels.includeClosedAttractions;

      checkbox.addEventListener('change', () => {
         onChange?.(checkbox.checked);
         rerunSearch?.();
      });

      label.append(checkbox, text);
      toggleWrap.appendChild(label);

      bodyEl?.insertBefore(toggleWrap, bodyEl.querySelector('.itin-search-input'));
   }
}
