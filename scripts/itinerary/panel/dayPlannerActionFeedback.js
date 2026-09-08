export class DayPlannerActionFeedback {
   static pendingDayPlannerActionFeedback = null;

   static setPendingDayPlannerActionFeedback(feedback) {
      DayPlannerActionFeedback.pendingDayPlannerActionFeedback = feedback;
   }

   static consumePendingDayPlannerActionFeedback() {
      const feedback = DayPlannerActionFeedback.pendingDayPlannerActionFeedback;
      DayPlannerActionFeedback.pendingDayPlannerActionFeedback = null;
      return feedback;
   }

   static resetPendingDayPlannerActionFeedback() {
      DayPlannerActionFeedback.pendingDayPlannerActionFeedback = null;
   }
}
