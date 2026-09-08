export class WizardControllerHelper {
   static async loadDefaultSelectionStepConfigs() {
      const { WizardSelectionStepFactory } = await import(
         './wizardSelectionStepFactory.js'
      );

      return WizardSelectionStepFactory.buildWizardSelectionStepConfigs();
   }

   static clearWizard(mountEl) {
      mountEl?.replaceChildren();
   }

   static closeWizard(mountEl) {
      WizardControllerHelper.clearWizard(mountEl);
   }
}
