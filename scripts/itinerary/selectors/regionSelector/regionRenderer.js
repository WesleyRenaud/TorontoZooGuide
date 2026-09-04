import { RegionSelection } from './regionSelection.js';

function createChoiceIndicator(isSelected) {
   const indicator = document.createElement('div');
   indicator.className = isSelected
      ? 'itin-add-btn is-added'
      : 'itin-add-btn';
   indicator.textContent = isSelected ? '−' : '+';

   return indicator;
}

function createChoiceRow({
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
   button.append(left, createChoiceIndicator(isSelected));

   return button;
}

export function buildRegionRows(region, selectedExhibitNames) {
   const exhibits = RegionSelection.getRegionExhibits(region);
   const regionName = RegionSelection.getRegionName(region);
   const regionSelected = RegionSelection.isRegionFullySelected(region, selectedExhibitNames);

   const rows = [
      createChoiceRow({
         label: regionName,
         isSelected: regionSelected,
         action: 'toggle-region',
         regionName,
      }),
   ];

   if (!RegionSelection.shouldHideDuplicateSingleExhibit(region)) {
      exhibits.forEach((exhibitName) => {
         rows.push(
            createChoiceRow({
               label: exhibitName,
               isSelected: selectedExhibitNames.has(exhibitName),
               action: 'toggle-exhibit',
               regionName,
               exhibitName,
            })
         );
      });
   }

   return rows;
}
