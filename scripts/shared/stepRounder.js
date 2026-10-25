export class StepRounder {
   static roundToStep(value, step) {
      return Math.round(value / step) * step;
   }
}
