import { ConsoleDateFieldBuilder } from './consoleDateFieldBuilder.js';
import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';
import { Strings } from '../../strings.js';

export class ConsoleDateRangeFieldsBuilder {
   static createDateRangeFields({
      startDateId,
      startLabel = Strings.labels.startDate,
      startPlaceholder = Strings.placeholders.startDate,
      startHelpText = '',
      endDateId,
      endLabel = Strings.labels.lastDay,
      endPlaceholder = Strings.placeholders.lastDay,
      endHelpText = '',
   } = {}) {
      return ConsoleFieldPrimitiveBuilder.createFragment([
         ConsoleDateFieldBuilder.createDateField({
            label: startLabel,
            inputId: startDateId,
            placeholder: startPlaceholder,
            helpText: startHelpText,
         }),
         ConsoleDateFieldBuilder.createDateField({
            label: endLabel,
            inputId: endDateId,
            placeholder: endPlaceholder,
            helpText: endHelpText,
         }),
      ]);
   }
}
