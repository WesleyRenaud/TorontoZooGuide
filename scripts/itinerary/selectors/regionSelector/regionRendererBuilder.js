export class RegionRendererBuilder {
   static createChoiceIndicator(isSelected) {
      const indicator = document.createElement('div');
      indicator.className = isSelected
         ? 'itin-add-btn is-added'
         : 'itin-add-btn';
      indicator.textContent = isSelected ? '−' : '+';

      return indicator;
   }

   static createChoiceRow({
      label,
      isSelected,
      action,
      regionName,
      exhibitName = '',
   }) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'itin-panel-item itin-region-choice-row';
      button.dataset.action = action;
      button.dataset.region = regionName;

      if (exhibitName) {
         button.dataset.exhibit = exhibitName;
      }

      const left = document.createElement('div');
      left.className = 'itin-panel-item-left';

      const text = document.createElement('div');
      text.className = 'itin-panel-text';

      const name = document.createElement('div');
      name.className = 'itin-panel-name';
      name.textContent = label;

      text.appendChild(name);
      left.appendChild(text);
      button.append(left, RegionRendererBuilder.createChoiceIndicator(isSelected));

      return button;
   }
}
