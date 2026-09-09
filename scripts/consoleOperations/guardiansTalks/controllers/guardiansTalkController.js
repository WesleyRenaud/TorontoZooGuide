import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { RecurringScheduleSetControllerFactory } from '../../forms/recurringScheduleSetControllerFactory.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { GuardiansTalkDropdownResetHelper } from '../helpers/guardiansTalkDropdownResetHelper.js';
import { Strings } from '../../../strings.js';

export class GuardiansTalkController {
   static createGuardiansTalkScheduleController({
      talkNameEl,
      locationEl,
      startDateEl,
      endDateEl,
      scheduleRowsEl,
      addScheduleRowEl,
      messageEl,
      talkLocationFilterController = null,
      ...controllerOptions
   } = {}) {
      return RecurringScheduleSetControllerFactory.createRecurringScheduleSetController({
         ...controllerOptions,
         scheduleRowsEl,
         addScheduleRowEl,
         startDateEl,
         endDateEl,
         messageEl,
         getSelectionValues: () => ({
            talk: ControllerHelper.getFieldValue(talkNameEl),
            location: ControllerHelper.getFieldValue(locationEl),
         }),
         validateSelection: ({ talk, location }) => {
            if (!location) {
               return Strings.validation.entityRequired(Strings.labels.location);
            }

            if (!talk) {
               return Strings.validation.entityRequired(Strings.labels.talkName);
            }

            return null;
         },
         resetSelection: () => {
            ControllerHelper.resetFormFields([locationEl, startDateEl, endDateEl, messageEl]);
            GuardiansTalkDropdownResetHelper.resetTalkDropdown({
               talkNameEl,
               talkLocationFilterController,
            });
         },
         prepareForm: async () => {
            if (talkLocationFilterController?.refreshLocations) {
               await talkLocationFilterController.refreshLocations();
            }
         },
         loadErrorMessage: Strings.loadErrors.locations,
         successMessage: result => Strings.status.guardiansTalkScheduleSaved(result),
         setSchedule: payload => ConsoleOperationsClient.setGuardiansTalkSchedule(payload),
         replaceOverlaps: payload => ConsoleOperationsClient.replaceGuardiansTalkScheduleOverlaps(payload),
         trimOverlaps: payload => ConsoleOperationsClient.trimGuardiansTalkScheduleOverlaps(payload),
      });
   }
}
