---
layout: blog
title: Tip of the Week 96 - Editorconfig
---

This post, for once, is not strictly about Puppet, but about a nice, standard way to customise the behaviour of a text editor directly from within your source code repository.

[Editorconfig](https://editorconfig.org/) is a file format that defines the coding style to use in an editor for the files of your repository.

It contains, in stanzas divided ini file format, various definitions to manage common editor settings:

  - `indent_style` - Indentation Style. Possible Values: tab, space
  - `indent_size` - Indentation Size (in single-spaced characters). Possible Values: an integer, tab
  - `tab_width` - Width of a single tabstop character. Possible Values: an integer (defaults to indent_size when indent_size is a number)
  - `end_of_line` - Line ending file format (Unix, DOS, Mac). Possible Values: lf, crlf, cr
  - `charset` - File character encoding. Possible Values: latin1, utf-8, utf-16be, utf-16le, utf-8-bom
  - `trim_trailing_whitespace` - Defines whether whitespace is allowed at the end of lines. Possible Values: true, false
  - `insert_final_newline` - Defines whether file should end with a newline. Possible Values: true, false

Some other settings are editor specific.

Editorconfig is supported by most of the existing editors either natively or via plugins.

Editors that support it out of the box: BBEdit, Codelite, elementaryCode, Builder, GitHub, Gogs, IntelliJidea, KText editor, Komodo, Kakoune, PyCharm, ReSharper, Rider, RubyMine, Source Lair, Tortoise Git, Visual Studio, Web Storm.

Editors that support it via a plugin: AppCode, Atom, Brackets, C Lion, Coda, Code::Block, Eclipse, Emacs, Geany, Gedit, jEdit, Micro, Net Beans, NodePad++, Php Storm, Sublime Text, Text Adept, Text Mate, Vim, Visual Studio Code.

An example is probably better than many works, so here's our `.editorconfig` file in our Psick control-repo. It applies to all the files of the repo, and, as you see, different settings can be defined according to the files name or extension.

    [*]
    charset = utf-8
    end_of_line = lf
    indent_style = space
    indent_size = 2
    insert_final_newline = true
    trim_trailing_whitespace = true

    [*.md]
    max_line_length = off
    trim_trailing_whitespace = false

Have fun with your editor, Puppet, life, universe and everything!

Alessandro Franceschi
