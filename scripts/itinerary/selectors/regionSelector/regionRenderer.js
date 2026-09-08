import { RegionRendererBuilder } from './regionRendererBuilder.js';
import { RegionStore } from './regionStore.js';

export class RegionRenderer {
   static buildRegionRows(region, selectedExhibitNames) {
      const exhibits = RegionStore.getRegionExhibits(region);
      const regionName = RegionStore.getRegionName(region);
      const regionSelected = RegionStore.isRegionFullySelected(region, selectedExhibitNames);

      const rows = [
         RegionRendererBuilder.createChoiceRow({
            label: regionName,
            isSelected: regionSelected,
            action: 'toggle-region',
            regionName,
         }),
      ];

      if (!RegionStore.shouldHideDuplicateSingleExhibit(region)) {
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
