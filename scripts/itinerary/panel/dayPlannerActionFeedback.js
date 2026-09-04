let pendingDayPlannerActionFeedback = null;

export class DayPlannerActionFeedback {
   static setPendingDayPlannerActionFeedback(feedback) {
      pendingDayPlannerActionFeedback = feedback;
   }

   static consumePendingDayPlannerActionFeedback() {
      const feedback = pendingDayPlannerActionFeedback;
      pendingDayPlannerActionFeedback = null;
      return feedback;
   }

   static resetPendingDayPlannerActionFeedback() {
      pendingDayPlannerActionFeedback = null;
   }
}
