---
layout: blog
title: example42 - Module Status update
---

The example42 modules received a larger update throughout the past couple of days:

  - update to make use of new travis infrastructure
  - add ruby 2.1.4 and puppet 4.2 rspec tests
  - lint cleaning
  - green travis spec tests

We are happy to announce that all example42 modules which we will keep updated are now in proper shape regarding spec tests and are ready to get used with puppet 4. (Note: see the following [list with example42 modules and deprecation status](https://github.com/example42/tp-playground/blob/master/bin/example42modules.txt))

We have not yet switched to new language features like type system and epp templates to allow compatibility with older puppet installations.
Within the next step we will upload new versions to puppet forge and afterwards increase version and make use of puppet 4 only language features.

Do not hesitate contacting us via [google group](mailto:example42-puppet-modules@googlegroups.com) in case of questions.

We are looking forward to seeing you in Portland at PuppetConf 2015.

Martin Alfke
