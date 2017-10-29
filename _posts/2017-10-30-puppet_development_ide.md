---
layout: blog
title: Tip of the Week 44 - Puppet Code Development IDE
---

How do you develop Puppet code? Which tools do you use? What tools should you use?

In the early days I was mostly using vim for any kind of code development. Basically this have been shell scripts, some ugly Perl code and rarely fixing some PHP code.
But: I have never been a developer.

When Puppet came into place I continued using vim also for Puppet code development. While writing code and learning new principles, I learned that pure vim is not really very helpful. Luckily there are extensions one can use like [puppet-vim](https://github.com/rodjek/vim-puppet).

Genereally you will never want to code Puppet without syntax highlighting and automatic indentation. 

But how to develop code on larger projects with multiple repositories? When asking an experienced developer one will immediately hear the term [IDE - Integrated development environment](https://en.wikipedia.org/wiki/Integrated_development_environment).

In the above mentioned case, we use vim as IDE.

But whet if you don't know vim? What other solutions are available? Let's check for some existing IDE's

### IDE's

Disclaimer: I am totally aware that this list is incomplete. It is a list of tools I had a look at.

#### Eclipse

The most common used IDE is [Eclipse](https://en.wikipedia.org/wiki/Eclipse_(software)). It is well known especially for Java development and has a huge set of extensions to be also useful on any other programming language.

#### Geppetto

Based on Eclipse the [Geppetto](https://github.com/puppetlabs/geppetto/wiki) IDE was put together. But Geppetto lacks all the new, modern Puppet features like lambdas, data types and tasks.

#### RubyMine

[JetBrains](https://www.jetbrains.com/) has multiple IDE's - partly Open Source, partly paid software - for different development purposes. The most known one is [IntelliJ IDEA](https://www.jetbrains.com/idea/). For Ruby based development [RubyMine](https://www.jetbrains.com/ruby/) is available. For Open Source development JetBrains grants [free licenses](https://www.jetbrains.com/community/support/#section=open-source) for Open Source projects.

#### XCode

When running OS X or MacOS it is also possible to use [XCode](https://en.wikipedia.org/wiki/Xcode). But XCode lacks full featured Puppet support.

#### Visual Studio Code

My personal favorite at the moment - next to vim - is [Visual Studio Code](https://en.wikipedia.org/wiki/Visual_Studio_Code) available for Linux, OS X, MacOS, Windows. VSCode has plenty of plugins for different development pruposes and multiple Version Control Systems. The most nice thing is that Puppet has officially released the [Puppet plugin for VSCode](https://puppet.com/blog/announcing-puppet-visual-studio-code).

#### Atom

Another IDE to use is [Atom](https://atom.io/) - an IDE developed by the people at [GitHub](https://github.com). Atom also has plenty of plugins which allow you to easily write code in many programming languages.

### Which one to use?

This basically depends on the Operating System which you have running. Most of the above mentioned IDE's work on Linux, macOS and Windows.
When people at customers ask us for a recommendation, we usually ask them whether their developers already have a license for a specific IDE or whether they have a preferred one. In this case we ask the Puppet developers to also make use of the same tool as there is already knowledge available.

When there is no common usage, one should check the [Wikipedia IDE](https://en.wikipedia.org/wiki/Integrated_development_environment#References) list or the [Comparison of integrated development environments](https://en.wikipedia.org/wiki/Comparison_of_integrated_development_environments).

Always check for usage conditions and licenses, get the download link and try which one you are most comfortable with.

Happy hacking on Puppet and [PSICK](https://github.com/example42/psick).

Martin Alfke
