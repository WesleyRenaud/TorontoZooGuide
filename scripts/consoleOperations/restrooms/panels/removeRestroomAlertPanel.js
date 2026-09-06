import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class RemoveRestroomAlertPanel {
   static createRemoveRestroomAlertPanel() {
      return Fragments.createPanelShell({
         panelId: 'removeRestroomAlertPanel',
         title: Strings.panelTitles.removeRestroomAlert,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.restroom,
               inputId: 'removeRestroomAlertRestroom',
               emptyOptionLabel: Strings.placeholders.restroom,
            }),
            Fragments.createActions({
               submitId: 'submitRemoveRestroomAlert',
               submitLabel: Strings.actions.removeAlert,
            }),
            Fragments.createStatus({
               statusId: 'removeRestroomAlertStatus',
            }),
         ],
      });
   }
}
