import { AmenityOpenPanelBuilder } from '../../forms/amenityOpenPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class ExhibitOpenView {
   static createExhibitOpenPanel() {
      return AmenityOpenPanelBuilder.createPanel({
         panelId: 'exhibitOpenPanel',
         title: Strings.panelTitles.exhibitOpen,
         entityLabel: Strings.entityLabels.exhibit,
         emptyOptionLabel: Strings.placeholders.exhibit,
         idPrefix: 'exhibitOpen',
         entityFieldName: 'Exhibit',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('exhibit'),
         submitId: 'submitExhibitOpen',
         statusId: 'exhibitOpenStatus',
      });
   }
}
