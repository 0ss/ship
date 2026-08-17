import { test } from "node:test";
import assert from "node:assert";
import {
  createInvite,
  acceptInvite,
  listInvites,
  setInviteSender,
  INVITE_TTL,
} from "./invites.js";

const sent = [];
setInviteSender(async (m) => sent.push(m));

test("create and accept", async () => {
  const t = await createInvite("a@b.com", "salah");
  assert.equal(acceptInvite(t).email, "a@b.com");
});

test("invite emails the invitee", async () => {
  sent.length = 0;
  const t = await createInvite("new@b.com", "salah");
  assert.deepEqual(
    sent.map((m) => [m.email, m.invitedBy, m.token]),
    [["new@b.com", "salah", t]],
  );
  acceptInvite(t);
});

test("invites expire after 30 days", async (t) => {
  assert.equal(INVITE_TTL, 30 * 24 * 60 * 60 * 1000);
  const token = await createInvite("old@b.com", "salah");
  const realNow = Date.now;
  Date.now = () => realNow() + INVITE_TTL + 1;
  try {
    assert.throws(() => acceptInvite(token), /invite expired/);
  } finally {
    Date.now = realNow;
  }
  // expired invite is gone, not resurrectable
  assert.throws(() => acceptInvite(token), /unknown invite/);
});

test("listInvites shows who invited who", async () => {
  const a = await createInvite("x@b.com", "salah");
  const b = await createInvite("y@b.com", "dana");
  const rows = listInvites().map((i) => [i.email, i.invitedBy]);
  assert.deepEqual(rows.slice(0, 2), [
    ["y@b.com", "dana"],
    ["x@b.com", "salah"],
  ]);
  assert.ok(listInvites().every((i) => i.expired === false));
  acceptInvite(a);
  acceptInvite(b);
});
