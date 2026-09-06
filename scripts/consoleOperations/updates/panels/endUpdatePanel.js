import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class EndUpdatePanel {
   static createEndUpdatePanel() {
      return Fragments.createPanelShell({
         panelId: 'endUpdatePanel',
         title: Strings.panelTitles.endUpdate,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.labels.update,
               inputId: 'endUpdateKey',
               emptyOptionLabel: Strings.placeholders.update,
            }),
            Fragments.createDateField({
               label: Strings.labels.endDate,
               inputId: 'endUpdateEndDate',
               placeholder: Strings.placeholders.endDate,
               helpText: Strings.help.endUpdateToday,
            }),
            Fragments.createActions({
               submitId: 'submitEndUpdate',
            }),
            Fragments.createStatus({
               statusId: 'endUpdateStatus',
            }),
         ],
      });
   }
}
