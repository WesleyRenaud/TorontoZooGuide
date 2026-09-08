import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';
import { ConsoleTextInputFieldBuilder } from '../../templates/consoleTextInputFieldBuilder.js';

export class CreateEventView {
   static createCreateEventPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'createEventPanel',
         title: Strings.panelTitles.createEvent,
         bodyChildren: [
            ConsoleTextInputFieldBuilder.createTextInputField({
               label: Strings.labels.name,
               inputId: 'createEventName',
               placeholder: Strings.textareas.eventNameExample,
            }),
            ConsoleTextInputFieldBuilder.createTextInputField({
               label: Strings.labels.location,
               inputId: 'createEventLocation',
               placeholder: Strings.textareas.eventLocationExample,
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.description,
               inputId: 'createEventDescription',
               placeholder: Strings.textareas.eventDescription,
            }),
            ConsoleTextInputFieldBuilder.createTextInputField({
               label: Strings.labels.link,
               inputId: 'createEventLink',
               placeholder: Strings.textareas.eventLinkExample,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'createEventStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'createEventEndDate',
               endHelpText: Strings.help.keepEventActiveWithoutEndDate,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitCreateEvent',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'createEventStatus',
            }),
         ],
      });
   }
}
