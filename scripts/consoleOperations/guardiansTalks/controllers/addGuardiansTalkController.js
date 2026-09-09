import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AddOccurrenceControllerFactory } from '../../forms/addOccurrenceControllerFactory.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { GuardiansTalkDropdownResetHelper } from '../helpers/guardiansTalkDropdownResetHelper.js';
import { Strings } from '../../../strings.js';

export class AddGuardiansTalkController {
   static createAddGuardiansTalkOccurrenceController({
      talkNameEl,
      locationEl,
      dateEl,
      timeEl,
      talkLocationFilterController = null,
      ...controllerOptions
   } = {}) {
      return AddOccurrenceControllerFactory.createAddOccurrenceController({
         ...controllerOptions,
         formFieldEls: [locationEl, dateEl, timeEl],
         resetSelection: () => {
            GuardiansTalkDropdownResetHelper.resetTalkDropdown({
               talkNameEl,
               talkLocationFilterController,
            });
         },
         getFormValues: () => {
            const time = ControllerHelper.getFieldValue(timeEl);

            return {
               talk: ControllerHelper.getFieldValue(talkNameEl),
               location: ControllerHelper.getFieldValue(locationEl),
               date: ControllerHelper.getFieldValue(dateEl),
               times: time ? [time] : [],
            };
         },
         validateForm: ({ talk, location, date, times }) => {
            const required = [
               [location, Strings.labels.location],
               [talk, Strings.labels.talkName],
               [date, Strings.labels.date],
               [times[0], Strings.labels.talkTime],
            ];

            for (const [value, label] of required) {
               if (!value) {
                  return Strings.validation.entityRequired(label);
               }
            }

            return null;
         },
         prepareForm: async () => {
            await talkLocationFilterController?.refreshLocations?.();
         },
         loadErrorMessage: Strings.loadErrors.locations,
         submitOccurrence: formValues => ConsoleOperationsClient.addGuardiansTalkOccurrence(formValues),
         successMessage: result => Strings.status.guardiansTalkOccurrenceAdded(result),
      });
   }
}
