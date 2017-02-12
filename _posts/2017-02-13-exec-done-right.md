---
layout: blog
title: Tip of the Week 7 - Using Exec resource the right way
---

exec { 'touch /tmp/foo': }

Ouch. Exec resource abusing seems to be an often used pattern.

Consider an Exec resource being an emergency exit. It is a powerful resource type that offers you to do almost anything to a system.

But please keep in mind that with great power comes great responsibility.

You (as the author of the Exec resource type declaration) are responsible for idempotency and error handling.

Best practice is to have an Exec resource for one-time commands only. This does not refer to a single puppet run, but throughout the life cycle of the system.

Don't forget to make use of the exec resource type parameters for idempotency:

  - onlyif
  - unless
  - refreshonly
  - creates

And don't forget to set the path parameter.

Martin Alfke
