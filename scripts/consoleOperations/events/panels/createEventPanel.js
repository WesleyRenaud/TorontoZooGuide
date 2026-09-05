import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createStatus,
   createTextareaField,
   createTextInputField,
} from '../../templates/fragments.js';

export class CreateEventPanel {
   static createCreateEventPanel() {
      return createPanelShell({
         panelId: 'createEventPanel',
         title: APP_STRINGS.panelTitles.createEvent,
         bodyChildren: [
            createTextInputField({
               label: APP_STRINGS.labels.name,
               inputId: 'createEventName',
               placeholder: APP_STRINGS.textareas.eventNameExample,
            }),
            createTextInputField({
               label: APP_STRINGS.labels.location,
               inputId: 'createEventLocation',
               placeholder: APP_STRINGS.textareas.eventLocationExample,
            }),
            createTextareaField({
               label: APP_STRINGS.labels.description,
               inputId: 'createEventDescription',
               placeholder: APP_STRINGS.textareas.eventDescription,
            }),
            createTextInputField({
               label: APP_STRINGS.labels.link,
               inputId: 'createEventLink',
               placeholder: APP_STRINGS.textareas.eventLinkExample,
            }),
            createDateRangeFields({
               startDateId: 'createEventStartDate',
               startHelpText: APP_STRINGS.help.startImmediately,
               endDateId: 'createEventEndDate',
               endHelpText: APP_STRINGS.help.keepEventActiveWithoutEndDate,
            }),
            createActions({
               submitId: 'submitCreateEvent',
            }),
            createStatus({
               statusId: 'createEventStatus',
            }),
         ],
      });
   }
}
