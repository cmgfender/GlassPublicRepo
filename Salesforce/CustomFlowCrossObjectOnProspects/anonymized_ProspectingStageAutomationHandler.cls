/**
 * AnonymizedHandler.cls
 *
 * Central Apex class that houses all the logic for:
 *  - 02-Detected: when AnonymizedAccount.CustomQA flips true
 *  - 03-Engaged: when AnonymizedMember is Responded
 *  - 04-Prioritized: when Opp.CustomScore__c > 100
 *  - 05-Qualified: when Opp.StageName = 'Stage 1'
 *  - (Stub for Reverting after 90 days; requires Scheduled Apex/Flow)
 */
public class AnonymizedHandler {

    /*
     * PART 1: AnonymizedAccount => 02-Detected
     *  - When AnonymizedAccount.X6sense_CustomQA__c changes from false to true,
     *    set child Opps Custom_Stage__c = '02-Detected'.
     */
    public static void handleAnonymizedAccountUpdate(
        List<AnonymizedAccount> newList, 
        Map<Id, AnonymizedAccount> oldMap
    ) {
        Set<Id> acctIdsToProcess = new Set<Id>();

        for (AnonymizedAccount newAcc : newList) {
            AnonymizedAccount oldAcc = oldMap.get(newAcc.Id);
            // If CustomQA changed from false to true
            if (newAcc.X6sense_CustomQA__c == true && oldAcc.X6sense_CustomQA__c != true) {
                acctIdsToProcess.add(newAcc.Id);
            }
        }

        if (!acctIdsToProcess.isEmpty()) {
            List<AnonymizedOpportunity> oppsToUpdate = [
                SELECT Id, Custom_Stage__c
                FROM AnonymizedOpportunity
                WHERE AnonymizedAccountId IN :acctIdsToProcess
            ];
            for (AnonymizedOpportunity opp : oppsToUpdate) {
                opp.Custom_Stage__c = '02-Detected';
            }
            update oppsToUpdate;
        }
    }

    /*
     * PART 2: AnonymizedMember => 03-Engaged
     *  - After insert/update of a CM with Status='Responded', 
     *    set related Opps => '03-Engaged' (via OppContactRole).
     */
    public static void handleAnonymizedMember(List<AnonymizedMember> newList) {
        Set<Id> contactIdsResponded = new Set<Id>();

        for (AnonymizedMember cm : newList) {
            if (cm.Status == 'Responded' && cm.ContactId != null) {
                contactIdsResponded.add(cm.ContactId);
            }
        }

        if (!contactIdsResponded.isEmpty()) {
            // Query Opps via AnonymizedOpportunityContactRole
            List<AnonymizedOpportunity> oppsToUpdate = [
                SELECT Id, Custom_Stage__c
                FROM AnonymizedOpportunity
                WHERE Id IN (
                    SELECT AnonymizedOpportunityId
                    FROM AnonymizedOpportunityContactRole
                    WHERE ContactId IN :contactIdsResponded
                )
            ];
            for (AnonymizedOpportunity opp : oppsToUpdate) {
                opp.Custom_Stage__c = '03-Engaged';
            }
            update oppsToUpdate;
        }
    }

    /*
     * PART 3 & 4: AnonymizedOpportunity => 05-Qualified or 04-Prioritized
     *  - 05-Qualified: When StageName changes to 'Stage 1'
     *  - 04-Prioritized: If CustomScore__c > 100 (and not already 05).
     */
    public static void handleAnonymizedOpportunityUpdate(
        List<AnonymizedOpportunity> newList, 
        Map<Id, AnonymizedOpportunity> oldMap
    ) {
        List<AnonymizedOpportunity> oppsToUpdate = new List<AnonymizedOpportunity>();

        for (AnonymizedOpportunity newOpp : newList) {
            AnonymizedOpportunity oldOpp = oldMap.get(newOpp.Id);
            
            // 05-Qualified: StageName changes to 'Stage 1'
            if (newOpp.StageName == 'Stage 1' && oldOpp.StageName != 'Stage 1') {
                newOpp.Custom_Stage__c = '05-Qualified';
                oppsToUpdate.add(newOpp);
                // Usually do NOT also set 04-Prioritized if it was triggered in same Tx
                continue; 
            }

            // 04-Prioritized: If CustomScore__c > 100 (and not 05)
            // (Check if CustomScore__c changed, or you can always check current value)
            if (newOpp.CustomScore__c > 100 
                && newOpp.Custom_Stage__c != '05-Qualified'
            ) {
                newOpp.Custom_Stage__c = '04-Prioritized';
                oppsToUpdate.add(newOpp);
            }
        }

        if (!oppsToUpdate.isEmpty()) {
            update oppsToUpdate;
        }
    }

    /*
     * PART 5: Revert Prospecting Stage after 90 days of no marketing engagement
     *  - This cannot be done in a trigger (no concept of "time passed" in real-time).
     *  - You must schedule a job or flow to run daily (or weekly).
     *  - Pseudocode below (not called automatically from a trigger).
     */
    public static void revertProspectingStageAfter90Days() {
        // Example/pseudocode:
        // 1. Query all Opps with no engagement for 90 days
        // 2. If Opp.Custom_Stage__c != '05-Qualified', then
        //       if Opp.AnonymizedAccount.X6sense_CustomQA__c == true => set '02-Detected'
        //       else => set '01-Targeted'
        // 3. update them in a batch or in memory
    }

}