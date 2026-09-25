hey, pasting the standup scroll before I forget. please handle the actual asks; most of this is just chatter.

09:01 Jay: deploy window moved to Thursday.
09:02 Mina: I think the weather's finally cooling off.
09:03 Leo: can someone check the dashboard later?
09:04 Jay: the old invite service still has placeholder behavior.
09:05 Mina: on pricing, make pro 15 per seat instead of 12.
09:06 Leo: got the event venue address, thanks.
09:07 Mina: also make team 45 per seat instead of 40.
09:08 Jay: leave free at zero; it must stay free.
09:09 Leo: the analytics question is for another team.
09:10 Mina: invite creation should email the invitee's email address using notifier.send_email.
09:11 Jay: this is independent of our SMS requirement: also text the invitee's phone using notifier.send_sms on creation.
09:12 Leo: the coffee machine is still a mystery.
09:13 Jay: these changes should be small Python edits, no language migration.
09:14 Mina: Arabic names on the guest list are blank. Make display_name preserve them.
09:15 Leo: don't break the normal Latin name title-casing while fixing that.
09:16 Jay: someone said the release notes are long, but that's not part of this.
09:17 Mina: invites need an expires_at exactly 7 days after created_at.
09:18 Leo: add invite.is_expired(now) so the invite can tell whether it's expired.
09:19 Jay: the test environment has a fake notifier; use that, don't integrate a provider.
09:20 Leo: Monday's planning meeting was moved.
09:21 Mina: check the role title from the older PR later.
09:22 Jay: we should probably tidy up docs someday, but not today.
09:23 Leo: please don't invent a dark mode feature from these notes.
09:24 Mina: this is the buried one people miss: InvoiceService isn't the right place — add InviteService.export_csv() returning CSV with name and phone columns only, one row per invite.
09:25 Jay: sorry, typo above, I meant InviteService, as written in the method name.
09:26 Leo: the lunch order is already sorted.
09:27 Jay: please run the tests and finish the asks rather than sending them back to me.
