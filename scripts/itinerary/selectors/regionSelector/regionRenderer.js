import { RegionRendererBuilder } from './regionRendererBuilder.js';
import { RegionSelection } from './regionSelection.js';

export class RegionRenderer {
   static buildRegionRows(region, selectedExhibitNames) {
      const exhibits = RegionSelection.getRegionExhibits(region);
      const regionName = RegionSelection.getRegionName(region);
      const regionSelected = RegionSelection.isRegionFullySelected(region, selectedExhibitNames);

      const rows = [
         RegionRendererBuilder.createChoiceRow({
            label: regionName,
            isSelected: regionSelected,
            action: 'toggle-region',
            regionName,
         }),
      ];

      if (!RegionSelection.shouldHideDuplicateSingleExhibit(region)) {
         exhibits.forEach((exhibitName) => {
            rows.push(
               RegionRendererBuilder.createChoiceRow({
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
}
