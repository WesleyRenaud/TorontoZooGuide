import { ConsoleCheckboxGridFieldBuilder } from './consoleCheckboxGridFieldBuilder.js';
import { Strings } from '../../strings.js';

export class ConsoleWeeklyScheduleCheckboxesBuilder {
   static createWeeklyScheduleCheckboxes({
      label = Strings.labels.openOnTheseDays,
      dayIds = {},
      includeHolidays = true,
   } = {}) {
      const options = [
         { id: dayIds.monday, label: Strings.schedule.dayLabels.monday },
         { id: dayIds.tuesday, label: Strings.schedule.dayLabels.tuesday },
         { id: dayIds.wednesday, label: Strings.schedule.dayLabels.wednesday },
         { id: dayIds.thursday, label: Strings.schedule.dayLabels.thursday },
         { id: dayIds.friday, label: Strings.schedule.dayLabels.friday },
         { id: dayIds.saturday, label: Strings.schedule.dayLabels.saturday },
         { id: dayIds.sunday, label: Strings.schedule.dayLabels.sunday },
      ];

      if (includeHolidays && dayIds.holidays) {
         options.push({
            id: dayIds.holidays,
            label: Strings.schedule.dayLabels.holidays,
         });
      }

      return ConsoleCheckboxGridFieldBuilder.createCheckboxGridField({
         label,
         options,
      });
   }
}
