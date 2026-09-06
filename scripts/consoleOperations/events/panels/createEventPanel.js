import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class CreateEventPanel {
   static createCreateEventPanel() {
      return Fragments.createPanelShell({
         panelId: 'createEventPanel',
         title: Strings.panelTitles.createEvent,
         bodyChildren: [
            Fragments.createTextInputField({
               label: Strings.labels.name,
               inputId: 'createEventName',
               placeholder: Strings.textareas.eventNameExample,
            }),
            Fragments.createTextInputField({
               label: Strings.labels.location,
               inputId: 'createEventLocation',
               placeholder: Strings.textareas.eventLocationExample,
            }),
            Fragments.createTextareaField({
               label: Strings.labels.description,
               inputId: 'createEventDescription',
               placeholder: Strings.textareas.eventDescription,
            }),
            Fragments.createTextInputField({
               label: Strings.labels.link,
               inputId: 'createEventLink',
               placeholder: Strings.textareas.eventLinkExample,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'createEventStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'createEventEndDate',
               endHelpText: Strings.help.keepEventActiveWithoutEndDate,
            }),
            Fragments.createActions({
               submitId: 'submitCreateEvent',
            }),
            Fragments.createStatus({
               statusId: 'createEventStatus',
            }),
         ],
      });
   }
}
