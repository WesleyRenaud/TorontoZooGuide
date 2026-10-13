import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class ExhibitClosedForSeasonView {
   static createExhibitClosedForSeasonPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'exhibitClosedForSeasonPanel',
         title: Strings.panelTitles.exhibitClosedForSeason,
         entityLabel: Strings.entityLabels.exhibit,
         emptyOptionLabel: Strings.placeholders.exhibit,
         idPrefix: 'exhibitClosedForSeason',
         entityFieldName: 'Exhibit',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepClosedUntilManuallyReopened('exhibit'),
         messageLabel: Strings.labels.closureMessage,
         messagePlaceholder: Strings.textareas.closureMessage,
         submitId: 'submitExhibitClosedForSeason',
         statusId: 'exhibitClosedForSeasonStatus',
      });
   }
}
