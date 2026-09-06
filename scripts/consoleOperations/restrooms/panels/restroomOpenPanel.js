import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class RestroomOpenPanel {
   static createRestroomOpenPanel() {
      return Fragments.createPanelShell({
         panelId: 'restroomOpenPanel',
         title: Strings.panelTitles.restroomOpen,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.restroom,
               inputId: 'restroomOpenRestroom',
               emptyOptionLabel: Strings.placeholders.restroom,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'restroomOpenStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restroomOpenEndDate',
               endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('restroom'),
            }),
            Fragments.createActions({
               submitId: 'submitRestroomOpen',
            }),
            Fragments.createStatus({
               statusId: 'restroomOpenStatus',
            }),
         ],
      });
   }
}
