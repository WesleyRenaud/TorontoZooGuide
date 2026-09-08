import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { ItineraryConfirmationResult } from '../itineraryConfirmationResult.js';
import { ScheduleItemConfirmationController } from './scheduleItemConfirmationController.js';

export class ScheduleItemConfirmationFlowHelper {
   static getConfirmationMountEl() {
      return ItineraryPanelFragment.getItineraryPanelMountEl() ?? document.body;
   }

   static requestScheduleItemConfirmation({
      showConfirmation,
      initialResult,
      request,
      confirmationOptions,
      confirmationProps = {},
      buildConfirmedOptions,
      beforeConfirm = async () => {},
      resolveConfirmErrorAsSaveFailed = false,
   }) {
      return new Promise((resolve) => {
         const confirm = async (confirmArgs = {}) => {
            await beforeConfirm(confirmArgs);

            const confirmedResult = await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation(
               request,
               {
                  ...confirmationOptions,
                  ...buildConfirmedOptions(confirmArgs),
               }
            );

            resolve(confirmedResult);
         };

         showConfirmation({
            ...confirmationProps,
            onConfirm: async (confirmArgs) => {
               if (!resolveConfirmErrorAsSaveFailed) {
                  await confirm(confirmArgs);
                  return;
               }

               try {
                  await confirm(confirmArgs);
               }
               catch (error) {
                  resolve(ScheduleItemConfirmationController.createScheduleItemSaveFailedResult());
               }
            },
            onCancel: () => {
               resolve(ItineraryConfirmationResult.createItineraryConfirmationCancelledResult(initialResult));
            },
         });
      });
   }
}
