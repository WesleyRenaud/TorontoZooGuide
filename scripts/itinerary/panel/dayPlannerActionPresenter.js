export class DayPlannerActionPresenter {
   static pendingDayPlannerActionFeedback = null;

   static setPendingDayPlannerActionFeedback(feedback) {
      DayPlannerActionPresenter.pendingDayPlannerActionFeedback = feedback;
   }

   static consumePendingDayPlannerActionFeedback() {
      const feedback = DayPlannerActionPresenter.pendingDayPlannerActionFeedback;
      DayPlannerActionPresenter.pendingDayPlannerActionFeedback = null;
      return feedback;
   }

   static resetPendingDayPlannerActionFeedback() {
      DayPlannerActionPresenter.pendingDayPlannerActionFeedback = null;
   }
}
