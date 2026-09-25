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
chat 01: the stage display is working again.
chat 02: the weekly sync got moved.
chat 03: thanks for checking yesterday.
chat 04: weather looks better for the event.
chat 05: the lunch poll closes at noon.
chat 06: design review is next week.
chat 07: we already answered the venue email.
chat 08: dashboard screenshots are in the other channel.
chat 09: the status page incident is closed.
chat 10: someone found the missing HDMI cable.
chat 11: the analytics team owns that chart.
chat 12: a past launch used the same venue.
chat 13: the projector has a spare bulb.
chat 14: the budget deck is in finance.
chat 15: the offsite RSVP list is current.
chat 16: the support queue is quiet.
chat 17: the branch name was shortened.
chat 18: the old mockups are archived.
chat 19: the room booking is confirmed.
chat 20: the calendar invite was updated.
chat 21: the stage display is working again.
chat 22: the weekly sync got moved.
chat 23: thanks for checking yesterday.
chat 24: weather looks better for the event.
chat 25: the lunch poll closes at noon.
chat 26: design review is next week.
chat 27: we already answered the venue email.
chat 28: dashboard screenshots are in the other channel.
chat 29: the status page incident is closed.
chat 30: someone found the missing HDMI cable.
chat 31: the analytics team owns that chart.
chat 32: a past launch used the same venue.
chat 33: the projector has a spare bulb.
chat 34: the budget deck is in finance.
chat 35: the offsite RSVP list is current.
chat 36: the support queue is quiet.
chat 37: the branch name was shortened.
chat 38: the old mockups are archived.
chat 39: the room booking is confirmed.
chat 40: the calendar invite was updated.
09:24 Mina: this is the buried one people miss: InvoiceService isn't the right place — add InviteService.export_csv() returning CSV with name and phone columns only, one row per invite.
09:25 Jay: sorry, typo above, I meant InviteService, as written in the method name.
09:26 Leo: the lunch order is already sorted.
09:27 Jay: please run the tests and finish the asks rather than sending them back to me.
chat 41: dashboard screenshots are in the other channel.
chat 42: the status page incident is closed.
chat 43: someone found the missing HDMI cable.
chat 44: the analytics team owns that chart.
chat 45: a past launch used the same venue.
chat 46: the projector has a spare bulb.
chat 47: the budget deck is in finance.
chat 48: the offsite RSVP list is current.
chat 49: the support queue is quiet.
chat 50: the branch name was shortened.
chat 51: the old mockups are archived.
chat 52: the room booking is confirmed.
chat 53: the calendar invite was updated.
chat 54: the stage display is working again.
chat 55: the weekly sync got moved.
chat 56: thanks for checking yesterday.
chat 57: weather looks better for the event.
chat 58: the lunch poll closes at noon.
chat 59: design review is next week.
chat 60: we already answered the venue email.
chat 61: dashboard screenshots are in the other channel.
chat 62: the status page incident is closed.
chat 63: someone found the missing HDMI cable.
chat 64: the analytics team owns that chart.
chat 65: a past launch used the same venue.
chat 66: the projector has a spare bulb.
chat 67: the budget deck is in finance.
chat 68: the offsite RSVP list is current.
chat 69: the support queue is quiet.
chat 70: the branch name was shortened.
chat 71: the old mockups are archived.
chat 72: the room booking is confirmed.
chat 73: the calendar invite was updated.
chat 74: the stage display is working again.
chat 75: the weekly sync got moved.
chat 76: thanks for checking yesterday.
chat 77: weather looks better for the event.
chat 78: the lunch poll closes at noon.
chat 79: design review is next week.
chat 80: we already answered the venue email.
