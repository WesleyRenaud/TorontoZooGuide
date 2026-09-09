import { ConsoleActionsBuilder } from '../templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../templates/consoleDateFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../templates/consoleStatusBuilder.js';

export class EndRecurringSchedulePanelBuilder {
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
      timesLabel,
      timesInputId,
      timesHelpText,
      endDateLabel,
      endDateInputId,
      endDatePlaceholder,
      endDateHelpText,
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
         ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
            label: timesLabel,
            inputId: timesInputId,
            helpText: timesHelpText,
         }),
         ConsoleDateFieldBuilder.createDateField({
            label: endDateLabel,
            inputId: endDateInputId,
            placeholder: endDatePlaceholder,
            helpText: endDateHelpText,
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
