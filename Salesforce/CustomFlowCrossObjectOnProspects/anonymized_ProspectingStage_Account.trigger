/**
 * ProspectingStage_AnonymizedAccount.trigger
 * 
 * Runs on AnonymizedAccount AFTER UPDATE,
 * delegates logic to the handler class.
 */
trigger ProspectingStage_AnonymizedAccount on AnonymizedAccount (after update) {
    AnonymizedHandler.handleAnonymizedAccountUpdate(Trigger.new, Trigger.oldMap);
}