import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class CreateUpdatePanel {
   static createCreateUpdatePanel() {
      return Fragments.createPanelShell({
         panelId: 'createUpdatePanel',
         title: Strings.panelTitles.createUpdate,
         bodyChildren: [
            Fragments.createTextInputField({
               label: Strings.labels.title,
               inputId: 'createUpdateTitle',
               placeholder: Strings.textareas.updateTitleExample,
            }),
            Fragments.createTextareaField({
               label: Strings.labels.description,
               inputId: 'createUpdateDescription',
               placeholder: Strings.textareas.updateDescription,
            }),
            Fragments.createSelectField({
               label: Strings.labels.type,
               inputId: 'createUpdateType',
               emptyOptionLabel: Strings.placeholders.type,
               options: [
                  ...Strings.updateTypes,
                  { value: Strings.labels.departure },
               ],
            }),
            Fragments.createDateRangeFields({
               startDateId: 'createUpdateStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'createUpdateEndDate',
               endHelpText: Strings.help.keepUpdateActiveWithoutEndDate,
            }),
            Fragments.createActions({
               submitId: 'submitCreateUpdate',
            }),
            Fragments.createStatus({
               statusId: 'createUpdateStatus',
            }),
         ],
      });
   }
}
