import { AmenityOpenPanelBuilder } from '../../forms/amenityOpenPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class RestroomOpenView {
   static createRestroomOpenPanel() {
      return AmenityOpenPanelBuilder.createPanel({
         panelId: 'restroomOpenPanel',
         title: Strings.panelTitles.restroomOpen,
         entityLabel: Strings.entityLabels.restroom,
         emptyOptionLabel: Strings.placeholders.restroom,
         idPrefix: 'restroomOpen',
         entityFieldName: 'Restroom',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('restroom'),
         submitId: 'submitRestroomOpen',
         statusId: 'restroomOpenStatus',
      });
   }
}
