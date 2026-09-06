import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class ExhibitOpenPanel {
   static createExhibitOpenPanel() {
      return Fragments.createPanelShell({
         panelId: 'exhibitOpenPanel',
         title: Strings.panelTitles.exhibitOpen,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'exhibitOpenExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'exhibitOpenStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'exhibitOpenEndDate',
               endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('exhibit'),
            }),
            Fragments.createActions({
               submitId: 'submitExhibitOpen',
            }),
            Fragments.createStatus({
               statusId: 'exhibitOpenStatus',
            }),
         ],
      });
   }
}
