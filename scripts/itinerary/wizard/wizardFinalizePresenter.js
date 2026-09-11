export class WizardFinalizePresenter {
   static shouldShowSaveIssuesPopup(savedItinerary) {
      return Boolean(savedItinerary?.saveIssues?.length);
   }
}
