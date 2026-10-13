import { AmenityOpenPanelBuilder } from '../../forms/amenityOpenPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class ExhibitOpenForSeasonView {
   static createExhibitOpenForSeasonPanel() {
      return AmenityOpenPanelBuilder.createPanel({
         panelId: 'exhibitOpenForSeasonPanel',
         title: Strings.panelTitles.exhibitOpenForSeason,
         entityLabel: Strings.entityLabels.exhibit,
         emptyOptionLabel: Strings.placeholders.exhibit,
         idPrefix: 'exhibitOpenForSeason',
         entityFieldName: 'Exhibit',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('exhibit'),
         submitId: 'submitExhibitOpenForSeason',
         statusId: 'exhibitOpenForSeasonStatus',
      });
   }
}
