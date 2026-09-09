import { ConsoleActionsBuilder } from '../templates/consoleActionsBuilder.js';
import { ConsolePanelShellBuilder } from '../templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../templates/consoleStatusBuilder.js';

export class CancelOccurrencePanelBuilder {
   static createPanel({
      panelId,
      title,
      locationLabel,
      locationInputId,
      locationEmptyOptionLabel,
      talkLabel,
      talkInputId,
      talkEmptyOptionLabel,
      entityLabel,
      entityInputId,
      entityEmptyOptionLabel,
      dateLabel,
      dateInputId,
      dateEmptyOptionLabel,
      timesLabel,
      timesInputId,
      timesHelpText,
      submitId,
      statusId,
   } = {}) {
      const bodyChildren = [];

      if (locationInputId && talkInputId) {
         bodyChildren.push(
            ConsoleSelectFieldBuilder.createSelectField({
               label: locationLabel,
               inputId: locationInputId,
               emptyOptionLabel: locationEmptyOptionLabel,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: talkLabel,
               inputId: talkInputId,
               emptyOptionLabel: talkEmptyOptionLabel,
            }),
         );
      }
      else {
         bodyChildren.push(
            ConsoleSelectFieldBuilder.createSelectField({
               label: entityLabel,
               inputId: entityInputId,
               emptyOptionLabel: entityEmptyOptionLabel,
            }),
         );
      }

      bodyChildren.push(
         ConsoleSelectFieldBuilder.createSelectField({
            label: dateLabel,
            inputId: dateInputId,
            emptyOptionLabel: dateEmptyOptionLabel,
         }),
         ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
            label: timesLabel,
            inputId: timesInputId,
            helpText: timesHelpText,
         }),
         ConsoleActionsBuilder.createActions({
            submitId,
         }),
         ConsoleStatusBuilder.createStatus({
            statusId,
         }),
      );

      return ConsolePanelShellBuilder.createPanelShell({
         panelId,
         title,
         bodyChildren,
      });
   }
}
