@isTest
private class AnonymizedHandlerTest {

    @isTest static void testAllAutomations() {

        // ======================================
        // 1) Setup a user to run as
        // ======================================
        Profile p = [SELECT Id FROM Profile WHERE Name = 'System Administrator' LIMIT 1];
        UserRole ur = new UserRole(Name = 'Test Role');
        insert ur;

        User testUser = new User(
            Alias = 'tstusr',
            Email = 'testuser@example.com',
            EmailEncodingKey = 'UTF-8',
            LastName = 'TestUser',
            LanguageLocaleKey = 'en_US',
            LocaleSidKey = 'en_US',
            ProfileId = p.Id,
            TimeZoneSidKey = 'America/Los_Angeles',
            UserName = 'testuser' + DateTime.now().getTime() + '@example.com',
            UserRoleId = ur.Id
        );
        insert testUser;

        System.runAs(testUser) {

            // ======================================
            // 2) Create AnonymizedAccount & AnonymizedOpportunity
            // ======================================
            AnonymizedAccount acct = new AnonymizedAccount(
                Name = 'Trigger Test AnonymizedAccount',
                X6sense_CustomQA__c = false  // Initial false
            );
            insert acct;

            AnonymizedOpportunity opp = new AnonymizedOpportunity(
                Name = 'Test Opp',
                AnonymizedAccountId = acct.Id,
                StageName = 'Prospecting',  // Some initial stage
                CloseDate = Date.today().addDays(30),
                Custom_Stage__c = '01-Targeted'
            );
            insert opp;

            // Verify initial stage
            System.assertEquals('01-Targeted', opp.Custom_Stage__c,
                'Initial Custom_Stage__c should be 01-Targeted');


            // ======================================
            // 3) Flip AnonymizedAccount.CustomQA to true => "02-Detected"
            // ======================================
            acct.X6sense_CustomQA__c = true;
            update acct;

            AnonymizedOpportunity oppAfterAcctUpdate = [
                SELECT Id, Custom_Stage__c 
                FROM AnonymizedOpportunity 
                WHERE Id = :opp.Id
            ];
            System.assertEquals('02-Detected', oppAfterAcctUpdate.Custom_Stage__c,
                'Opp should become 02-Detected when CustomQA flips to true');


            // ======================================
            // 4) Test AnonymizedMember => "03-Engaged"
            // ======================================
            // create Contact + OppContactRole + AnonymizedMember(Status=Responded)
            Contact c = new Contact(FirstName = 'Test', LastName='Contact', AnonymizedAccountId=acct.Id);
            insert c;

            AnonymizedOpportunityContactRole ocr = new AnonymizedOpportunityContactRole(
                AnonymizedOpportunityId = opp.Id,
                ContactId = c.Id,
                Role = 'Influencer',
                IsPrimary = true
            );
            insert ocr;

            Campaign camp = new Campaign(Name = 'Test Campaign', IsActive = true);
            insert camp;

            // Insert a responded campaign member
            AnonymizedMember cm = new AnonymizedMember(
                CampaignId = camp.Id,
                ContactId = c.Id,
                Status = 'Responded'
            );
            insert cm; 
            // AFTER INSERT on AnonymizedMember => sets Opp => '03-Engaged'

            AnonymizedOpportunity oppAfterCM = [
                SELECT Id, Custom_Stage__c 
                FROM AnonymizedOpportunity 
                WHERE Id = :opp.Id
            ];
            System.assertEquals('03-Engaged', oppAfterCM.Custom_Stage__c,
                'Opp should become 03-Engaged when AnonymizedMember is Responded');


            // ======================================
            // 5) CustomScore__c > 100 => "04-Prioritized"
            // ======================================
            oppAfterCM.CustomScore__c = 110; // set a custom field
            update oppAfterCM; 
            // AFTER UPDATE => triggers handleAnonymizedOpportunityUpdate => "04-Prioritized"

            AnonymizedOpportunity oppAfterScore = [
                SELECT Custom_Stage__c, CustomScore__c
                FROM AnonymizedOpportunity
                WHERE Id = :opp.Id
            ];
            System.assertEquals('04-Prioritized', oppAfterScore.Custom_Stage__c,
                'Opp should become 04-Prioritized if CustomScore__c > 100');


            // ======================================
            // 6) Change StageName => 'Stage 1' => "05-Qualified"
            // ======================================
            oppAfterScore.StageName = 'Stage 1';
            update oppAfterScore; 
            // AFTER UPDATE => triggers handleAnonymizedOpportunityUpdate => "05-Qualified"

            AnonymizedOpportunity oppAfterStage1 = [
                SELECT Custom_Stage__c, StageName
                FROM AnonymizedOpportunity
                WHERE Id = :opp.Id
            ];
            System.assertEquals('05-Qualified', oppAfterStage1.Custom_Stage__c,
                'Opp should become 05-Qualified when StageName changes to Stage 1');

            // (Optional) You could test the "Reverting after 90 days" 
            // by calling AnonymizedHandler.revertProspectingStageAfter90Days()
            // after creating data that meets 90-days criteria, 
            // but that is typically a separate test or a scheduled apex test.
        }
    }
}