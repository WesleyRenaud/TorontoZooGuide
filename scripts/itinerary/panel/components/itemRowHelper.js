import { SpeciesLinkTitleBuilder } from '../../../animals/speciesLinkTitleBuilder.js';

export class ItemRowHelper {
   static createItemNameElement({
      name,
      nameSuffix = '',
      species,
      enclosureName,
      onNameClick,
   } = {}) {
      if (species !== undefined) {
         return SpeciesLinkTitleBuilder.createAnimalTitleLinkElement({
            species,
            enclosureName,
            className: 'itin-panel-name',
            onClick: onNameClick,
         });
      }

      return SpeciesLinkTitleBuilder.createSpeciesLinkTitleElement({
         text: name,
         suffix: nameSuffix,
         className: 'itin-panel-name',
         onClick: onNameClick,
      });
   }
}
