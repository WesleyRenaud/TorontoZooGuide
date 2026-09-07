import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { ItineraryConfirmationResult } from '../itineraryConfirmationResult.js';
import { ScheduleItemConfirmationFlow } from './scheduleItemConfirmationFlow.js';

export class ScheduleItemConfirmationFlowHelpers {
   static getConfirmationMountEl() {
      return ItineraryPanelPopup.getItineraryPanelMountEl() ?? document.body;
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

            const confirmedResult = await ScheduleItemConfirmationFlow.scheduleItineraryItemWithConfirmation(
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
                  resolve(ScheduleItemConfirmationFlow.createScheduleItemSaveFailedResult());
               }
            },
            onCancel: () => {
               resolve(ItineraryConfirmationResult.createItineraryConfirmationCancelledResult(initialResult));
            },
         });
      });
   }
}
