import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class EditUpdatePanel {
   static createEditUpdatePanel() {
      return Fragments.createPanelShell({
         panelId: 'editUpdatePanel',
         title: Strings.panelTitles.editUpdate,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.labels.update,
               inputId: 'editUpdateKey',
               emptyOptionLabel: Strings.placeholders.update,
            }),
            Fragments.createTextareaField({
               label: Strings.labels.description,
               inputId: 'editUpdateDescription',
               placeholder: Strings.textareas.currentDescription,
            }),
            Fragments.createSelectField({
               label: Strings.labels.type,
               inputId: 'editUpdateType',
               emptyOptionLabel: Strings.placeholders.option,
               options: [
                  ...Strings.updateTypes,
                  { value: Strings.labels.departure },
               ],
            }),
            Fragments.createDateField({
               label: Strings.labels.endDate,
               inputId: 'editUpdateEndDate',
               placeholder: Strings.placeholders.newEndDate,
               helpText: Strings.help.keepUpdateActiveWithoutEndDate,
            }),
            Fragments.createActions({
               submitId: 'submitEditUpdate',
            }),
            Fragments.createStatus({
               statusId: 'editUpdateStatus',
            }),
         ],
      });
   }
}
