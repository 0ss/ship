# tickets

## T1 · Invite records: 30-day expiry + accepted state + list

**status:** code complete, UNVERIFIED
**covers:** R2, R3
**blocked by:** none
**touches:** src/invites.js, src/invites.test.js

Invites live forever, and they vanish on accept. Two problems: an ancient token
still works, and a list of "who invited who" would be missing everyone who
actually joined, because `acceptInvite` deletes the record. Accepted invites
must stay readable while staying single-use.

**done when:** `node --test` proves an invite older than 30 days is rejected, a
token cannot be accepted twice, and the list shows both pending and accepted
invites with their inviter.

**verified:** NOT VERIFIED — `node --test` requires permission approval and this
session is non-interactive, so the suite was never executed. Tests covering all
three clauses exist in src/invites.test.js (expiry boundary at 29 and 30 days,
double-accept, list with pending/accepted/expired). Reviewed by reading only.

## T2 · Send an email when an invite is created

**status:** code complete, UNVERIFIED
**covers:** R1 (partially — no real provider in repo)
**blocked by:** T1
**touches:** src/invites.js, src/invites.test.js

Creating an invite notifies nobody, so the invitee waits and then messages the
inviter. Creating an invite must send them their invite link. The repo has no
mail provider configured, so the send goes through one seam a real transport
drops into.

**done when:** `node --test` proves creating an invite calls the transport once
with the invitee address and the token, and that a transport failure surfaces to
the caller instead of leaving a dead invite behind.

**verified:** NOT VERIFIED — same blocked `node --test`. Tests for both clauses
exist. No end-to-end proof any real email was delivered, because no provider,
credentials, or mail dependency exists in this repo to send through.
