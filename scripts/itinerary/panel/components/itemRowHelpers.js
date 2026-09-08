import { CreateSpeciesLinkTitle } from '../../../animals/createSpeciesLinkTitle.js';

export class ItemRowHelpers {
   static createItemNameElement({
      name,
      nameSuffix = '',
      species,
      enclosureName,
      onNameClick,
   } = {}) {
      if (species !== undefined) {
         return CreateSpeciesLinkTitle.createAnimalTitleLinkElement({
            species,
            enclosureName,
            className: 'itin-panel-name',
            onClick: onNameClick,
         });
      }

      return CreateSpeciesLinkTitle.createSpeciesLinkTitleElement({
         text: name,
         suffix: nameSuffix,
         className: 'itin-panel-name',
         onClick: onNameClick,
      });
   }
}
